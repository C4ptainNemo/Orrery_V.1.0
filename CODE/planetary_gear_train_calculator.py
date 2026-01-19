import math


def search_planet_gears(ratio:float=1.0,
                        tolerance:float=0.01,
                        annular_gear_pitch_diameter:float=100.0,
                        min_gear_teeth:int=10,
                        Z3_min:int=10,
                        min_gear_modulus:float=1.0,
                        max_gear_modulus:float=10.0,
                        mesh_efficiency:float=1.0,
                        member_function:str="13",
                        configuration:str="1AI"):
    """
    Searches for a planetary gear train for a specfic gear ratio.

    Args:
        ratio (float): Normalised gear ratio, input/output
        tolerance (float): The percentage error tolarance between the given ratio and accepetable ratios
        annular_gear_pitch_diameter (float): Pitch diameter in mm of the annular gear. Used to determine condition of neighbouring.
        min_gear_teeth (int): The minimum number of teeth any gear can have.
        min_gear_modulus (float): The minimum gear modulus in mm that any gear can have.
        member_function (str): What type of member function is the planetary train have. Options are "13", "31", "1v", "v1", "3v" and "v3".
            1, 3 represent the non-planet gears and v the carrier. The order is input-output, the other is held at rest.
        Configuration (str): What configuratio does the gear train have. Options are "1AI", "2AI", "2AA", "2II".

    Returns:
        String containing the details of a gear train will a ratio within the acceptable tolerance.
        Ratio: The calculated ratio for the gear train.
        Error: Percentage error with the given ratio.
        Z1: The number of teeth on the sun gear.
        Z2a: The number of teeth on the planet gear that meshes with the sun gear.
        Z2b: The number of teeth on the planet geat that meshes with the annular gear.
        Z3: The number of teeth on the annular gear.
        Modulus_Z1: The gear modulus of the sun gear and its planet gear.
        Modulus_Z3: The gear modulus of the annular gear and its planet gear.
    """
    # Parameters
    number_of_planet_gears = 3 # The number of planet gears the gear train will have
    f = 2 # mm, minimum distance between the edges of planet gears
    max_gear_teeth:int = int(annular_gear_pitch_diameter / min_gear_modulus)

    
    Z3_max = min(int(annular_gear_pitch_diameter / min_gear_modulus), max_gear_teeth) # Get the maximum number of teeth for the annular gear
    Z2_max = min(int(0.45 * annular_gear_pitch_diameter / min_gear_modulus - 2), max_gear_teeth) # Get the maximum number of teeth the planet geas can have using the minimum modulus and gears being 0.45 the sun gears pitch diameter.
    Z1_max = min(int((0.9 * annular_gear_pitch_diameter / min_gear_modulus) - (2 * min_gear_teeth) - 4), max_gear_teeth) # The maximum number of teeth the sdun gear can have.

    print("Begining Search...")
    print(f"Z1_max={Z1_max}, Z2_max={Z2_max}, Z3_max={Z3_max}\n")
    for Z3 in range(Z3_min, Z3_max + 1):
        print(f"Z3 = {Z3}") # Can uncomment to see progress
        for Z2a in range(min_gear_teeth, Z2_max + 1):
            for Z2b in range(min_gear_teeth, Z2_max + 1):
                for Z1 in range(min_gear_teeth, Z1_max + 1):
                    
                    # Assembly Condition
                    k:float = ((Z1 * Z2b) - (Z2a * Z3)) / (math.gcd(Z2a, Z2b) * number_of_planet_gears)
                    if not k.is_integer() : continue # If k is not an integer then end iteration

                    # Condition of Neighbouring
                    modulus_Z1:float = 0.0 # Set as zero to indicate its wrong if this is output at the end
                    modulus_Z3:float = 0.0

                    if configuration == "1AI":
                        if Z2a != Z2b: continue
                        modulus_Z3 = annular_gear_pitch_diameter / Z3
                        modulus_Z1 = modulus_Z3
                        if not Z1 + 2 * Z2a == Z3: continue
                    elif configuration == "2AI":
                        modulus_Z3 = annular_gear_pitch_diameter / Z3
                        modulus_Z1 = modulus_Z3 * (Z3 - Z2b) / (Z1 + Z2a)
                        if (modulus_Z1 * Z1) + (2 * modulus_Z1 * Z2a) > annular_gear_pitch_diameter: continue
                        if (modulus_Z3 * Z2b) > 0.45 * annular_gear_pitch_diameter: continue
                        if modulus_Z1 * (Z1 + Z2a) + modulus_Z3 + Z2b > annular_gear_pitch_diameter: continue
                    elif configuration == "2AA":
                        modulus_Z3 = min_gear_modulus
                        modulus_Z1 = modulus_Z3 * (Z3 + Z2b) / (Z1 + Z2a)
                        if modulus_Z1 * (Z1 + Z2a) > annular_gear_pitch_diameter: continue
                        if modulus_Z3 * (Z3 + Z2b) > annular_gear_pitch_diameter: continue
                    elif configuration == "2II":
                        if Z1 - Z2a == 0: continue # Prevents divide by zero error
                        modulus_Z1 = modulus_Z3 * (Z3 - Z2b) / (Z1 - Z2a)
                        if modulus_Z1 * Z1 > annular_gear_pitch_diameter: continue
                        if modulus_Z3 * Z3 > annular_gear_pitch_diameter: continue
                    else:
                        raise(ValueError("Configuration not valid"))

                    if modulus_Z1 < min_gear_modulus or modulus_Z1 > max_gear_modulus: continue
                    if modulus_Z3 < min_gear_modulus or modulus_Z3 > max_gear_modulus: continue

                    
                    # Check to see if the planets are too large and will contact each other
                    A2a = (modulus_Z1 * Z1 + modulus_Z1 * Z2a) / 2 # Distance between center axis and center of planet gear
                    A2b = (modulus_Z3 * Z3 + modulus_Z3 * Z2b) / 2
                    L2a = 2 * A2a * math.sin(math.pi / number_of_planet_gears) # Distance between centers of planet gears
                    L2b = 2 * A2b * math.sin(math.pi / number_of_planet_gears)
                    D2a = modulus_Z1 * Z2a # Diameter of the planet gear
                    D2b = modulus_Z3 * Z2b
                    if (D2a + f > L2a) or (D2b + f > L2b): continue

                    # Calculate Ratio for the given member function. Will check in the order if "any" is given.
                    # Taken from Gears and Gear Drives - Damir T Jelaska, page 337.
                    i:float = 0.0
                    efficiency:float = 0.0
                    u = (Z2a * Z3) / (Z2b * Z1)
                    if member_function == "13":
                        i = u
                        efficiency = mesh_efficiency
                    elif member_function == "31":
                        i = abs(1 / u)
                        efficiency = mesh_efficiency
                    elif member_function == "1v":
                        i = abs(1 - u)
                        if u == 1: efficiency = 0.0
                        else: efficiency = (1 - (u * mesh_efficiency)) / (1 - u)
                    elif member_function == "v1":
                        if 1 - u == 0: continue # Prevents divide by zero error
                        i = abs(1 / (1 - u))
                        if (1 - (u / mesh_efficiency)) == 0: efficiency = 0.0
                        else: efficiency = (1 - u) / (1 - (u / mesh_efficiency))
                    elif member_function == "3v":
                        i = 1 - (1 / u)
                        if u - 1 == 0: efficiency = 0.0
                        elif configuration == "2AA" or configuration == "2II":
                            efficiency = (u - (1 / mesh_efficiency)) / (u - 1)
                        elif configuration == "2AI" or configuration == "1AI":
                            efficiency = (u - mesh_efficiency) / (u - 1)
                    elif member_function == "v3":
                        if u - 1 == 0: continue # Prevents divide by zero error
                        i = abs(u / (u - 1))
                        if configuration == "2AA" or configuration == "2II":
                            if u - mesh_efficiency == 0: continue
                            else: efficiency = (u - 1) / (u - mesh_efficiency)
                        elif configuration == "2AI" or configuration == "1AI":
                            if (u - (1 / mesh_efficiency)) == 0: continue
                            else: efficiency = (u - 1) / (u - (1 / mesh_efficiency))
                    else:
                        raise(ValueError("Member function not valid"))
                    
                    # Percentage error between calculated ratio and desired ratio
                    error = round(abs((i - ratio) / ratio * 100), 6)
                    
                    if error < tolerance:
                        print(f"Ratio={round(i, 6)}, Config={configuration}, Member Function={member_function}, Error={error}, Num. Planets = {number_of_planet_gears}")
                        print(f"Z1={Z1}, Z2a={Z2a}, Z2b={Z2b}, Z3={Z3}")
                        print(f"D1={Z1 * modulus_Z1}, D2a={Z2a * modulus_Z1}, D2b={Z2b * modulus_Z3}, D3={Z3 * modulus_Z3}")
                        print(f"Modulus_Z1={modulus_Z1}, Modulus_Z3={modulus_Z3}, Efficiency={efficiency:.3f}", end="\n\n")
    
    print("Search complete")

search_planet_gears(ratio=6.5, 
                    tolerance=0.1, 
                    annular_gear_pitch_diameter=125,
                    min_gear_teeth=12,
                    Z3_min=12,
                    min_gear_modulus=2,
                    max_gear_modulus=3,
                    mesh_efficiency=0.9,
                    member_function="1v",
                    configuration="2AA")