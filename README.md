# Hackathon Solution
> BOSCH Hackaton Nov 2021
```diff
! All work dedicated to Bosch Hakathon 2021
```
- [x] CPP code for Sensors simulation with Aurdino
- [x] Python file for object location finding using Cross and Direcht echo

# Problem Statement
Nearest object detection with Ultrasonic Sensor in Car rare Bumper

#  How object distance calculated by Ultrasonic waves?

Direct echo mean when signal reflects back at 90 angle. The distance for direct echo can be calculated with the following formula:
```
Distance D = 1/2 × T × C
```
where D is the distance, T is the time between the emission and reception, and C is the sonic speed. (The value is multiplied by 1/2 because T is the time for go-and-return distance.) <br>
<img src="https://user-images.githubusercontent.com/56737996/143319640-90388853-f3eb-4fcd-b3b8-1430f5b498a4.gif" width="500" height="300">


# Methdology

Divided into foloowing two Steps
## A) When object is infront of Sensor (Direct Echo)
Direct echo is measured when waves strikes over object and bounce back perpendicularly. In this case simple formula applied 
```
Distance D = 1/2 × T × C
```
Co-ordinates/ location of object calculated by adding Distance **(D)** into  into **X-axis** and location of sensor into **Y-axis** 
```
X-axis = X + D
Y-axis = Sy    (relevent sensor's y coordinates)
```
## B) When object is not infront of sensor (Cross Echo)
This is bit tricky to find real distance when object is slightly tilted from direct face of sensor. when sensors propagate waves it bounce back to all directions and few of sensors catch signals depend upon direction of object. So, I simply draw a detailed figure of Trignometric Use of angles and sides of Triangle for real distance calculation. below is sketch have a look into:
![main2](https://user-images.githubusercontent.com/56737996/143722342-70dae530-771d-4ea3-af7f-975f88b6295c.png)

Here steps to calculate real distance by cross echo:
1. Calculate angle between ***d1*** and ***dist*** by ***inverse COS*** folrmula calculated above
2. Calculate **alpha** by using Triangle theorem (***The height drawn from a vertex to the hypotenuse divides a right angled triangle into two triangles that are both similar to the original triangle.***)  
3. Calculate **X** by using ***tan*** relation. 




## Visual Explanatioon Demo (Simulation)

let's have a look inside working on **youtube** [Software Solution Bosch](https://pages.github.com/).
# what unique?
- [x] Clean and Understandable code with less comments
- [x] Clean code
- [ ] Performance time boosting
- [x] Coded over real ultasonic sensors as well (file in CPP)

# Take away
thanks Bosch for providing such opportunity to work on :tada:
![bosch_logo](https://user-images.githubusercontent.com/56737996/142710244-7c7ecb4a-22a2-459b-b1a4-ebc47d0cbfdd.png)

**Author : Shoaib Ali <br>
Email: m.shoaib_ali@outlook.com**
<!-- This content will not appear in the rendered Markdown -->
