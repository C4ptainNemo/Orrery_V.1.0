# Orrery Version 1.0
![orrery_v1](https://github.com/user-attachments/assets/cf311299-b3cc-4aeb-ba29-672896dedcd2)
![orrery_v1_no_top](https://github.com/user-attachments/assets/f9ef8edb-0212-404f-84ec-17a4f3f0bd3b)

This repository is used to showcase the first completed version of my orrery.

The planets move on what is in escense slew rings, i.e. bearings with one of the rings having gear teeth to allow it to be driven. There are four sets of rings, each having a static ring that is mounted to the base, and two rotating rings, one per planet. These four sets of two make up the eight planets, Mercury & Venus, Earth & Mars, Jupiter & Saturn, Uranus & Neptune.

The gearing for the planets is also divided into the inner and outer planets. This is due to the large difference between their orbital periods. There is a main driving gear which meshed with different sets of gears that give the correct reduction to have accurate oribital periods. The outer planets have an additional planetary gear reducer (26 times reduction) between the main driving gear and their input gears.




## Thoughts and Improvements
Since each planets reducing gears are independent of each other, finding the correct gear ratios is simple, with a brute force check of combinations working fine. However this means that there are a lot of gears, since each planet has 3-5 gears to give the reduction and spacing needed. Improvements can be made to the layout of the gears to reduce the need for idler gears. 

Due to uncertaity of the ability to 3D print bevel gears, spur gears were used for the planet rings themselves. This added the limitation that there needs to be space between the adjectent rings to fit planet rings driving gear, which meant the planet ring gears were much larger than they otherwise need to be. Testing to find suiatble methods of printing bevel gears should be done to remove this issue.

A thought I had to reduce the number of gears needed is to have the reduction happen in a chain, instead of having seperate sets of gears for each planet. The difference in period between adjecent planets is around 2-3 except Mars to Jupiter which is about 6:1. So the orbital periods of each planet would be normalised by dividing its orbital period by Mercurys (so Mercury has a period of 1). So by doing the reduction in a chain, an approximately 2:1 reduction is needed coming from Uranus for Nepotune instead of 700:1.
