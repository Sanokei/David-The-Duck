# David the Duck
a project for a dear friend in which a duck she drew goes on adventures on her screen.

## Day 0 (8/2)
using gifs as part of the animation
or using pics in sequence to make it so i can add movement

went with the latter.
add complete feature set later.

## Day 1 (8/3)
-move notepads
-memes?
-games:
+play ball? (haha)
+
-leave food by clicking and stuff
- be cute (thats a given)

im stuck, idk wat i did but now what worked before isnt working now and its killing me

nvm it was me just moving files around and the files werent pathed

now only 1.6.3 and i got it to work but the transparent background is no longer transparent? might be an issue with changing the gif files
to the png files.

having trouble with it only half working with notebook files, but thats not really important

ffs and thats just great, it doesnt want to work at all now. perfect.

so i thought it was because i made png files out of dave, instead of gif files so i changed it to gifs 
but that did nothing, back to the drawing board.

im trying to debug, but the worst part about finding a problem is that there isnt a problem.

idk wats going on

OH MY FUCKING GOD, i think i figured it out?
no

but i took a breather and i messed up. I switched width with height

but again, that didnt solve much.

fixed some things, but still, i saw david the duck for a split second, but then it didnt work.

idk wats going on at this point.

okay so it has to do with the actions.
cuz i commented it out and the idle animation worked fine.

realized that when reading from config, it doesnt convert over type, was passing a binary string as a interger which made exponential numbers

well even then, the actions still dont seem to be working.

omg im stupid

when you work with anything remember to merge your multiple branches.
I forgot to merge a bug fix over to another version of my code. thats why it wasnt working. this whole time.

## Day 2 (8/4)

FUCKING was the first auto correct thing that notepad expected me to say, so ill just keep it.
what i was trying to say was fixed
I fixed a lot of the small things that werent working, like david being able to leave the main screen.

im starting super late, so i have no real time to work on this, thinking of the time i have left, which is around 
3 days, i think im going to just try to get all the small things working and work outwards from there.

I moved the creation of the canvas to outside the animation creator, because it was creating multiple canvases
which is an error.

adding everything to a config made this easy.. easier.

I plan to update the weights so that it biases opposite effects. e.g (if sleep, dont sleep as much. if go left, more often go right)

But from here we have reached 2.0.0

im so tired i forgot to put the file type it was suppose to be .gif not just blank

The x and y cords were broken, so instead of saving them myself, i used rootx and rooty of the api to get the window
position.
Ironically, this broke the move function, which relys on the cords, possibly it has to do with how the window x and y are calculated.
or it could be that i somehow go out of bounds of the screen without knowing.

The movement up and down are diffent from side to side for some reaosn.
it should be easy
but it glitches.

i think i fixed it? its hard to tell

simple change for rootx -> rooty 
realized the speed and time could be 0 so i just add 1 so that doesnt happen

slimmed down the import from * (all) to the select classes needed.

adding new feature in which reddit gets displayed on a window and gets pushed into the screen

## Day 3 (8/5)
I have two days remaining.

I have to figure out what is vital and what to cut.

I decided to continue the reddit get thing. But I think a random youtube video getting played and sent via duck is better.
so I will be working on that.

scratch the creating a new window portion. It makes it very complicated. Imma spawn a new webBrowser off screen.

I did nothing today to work on this. oops.

Well its 11:05 and i didnt want to work on it because the errors i faced meant i would have to go into the 
deep and scary world of... multi threading *shivers*

okay so i just set up the threads but then i read through it and i should be using processes instead which are quite simialr
so im not too upset about changing it last minute.

## Day 4 (8/6)

One day until its Cons birthday, i gotta make it count.

im going insane.

so apparently processes dont work with the window api im using because of something with pickle.

okay so instead imma just have a simple nested for loop. 

instead of going one direction, im going to make it so that it goes to a point on the screen.

okay this is hours later with a new version. 

I deleted how it moves all together now it gets a point on the screen
Let that be B
David is at A
it gets the distance, let that be dy
and then get all the frames possible between these two points. then from there it creates an animation loop
that coresponds to the number of aviable frames.
it travels the incrimiate distance on the line 
getting the x and y incrimant from
```
y = slope * (The incriment * current frame)
x = Square_root_of((The incriment * current frame)^2 + y)
```
then i just add the x and y to themselves so that i dont do the same math again from that new point

if i did that it would go on forever, being very small
its like cutting a race in half then cutting it again over and over

i multiplied by the slope instead of getting the angle via arctan, it should work now.

i forgot how much im bad at math ;-;

okay so i was trying to get perma versions of x and y
i created perma and perm i just screamed into my pillow
this whole time
this error
has been a typo
i want to die

im so dumb.
im so so dumb.
im a stupid man.

this is why coding tired isnt good.

i dont need all that math.

since i know the ending location
i cant just add incrimint ammounts to x and y.

this day has been hell.

