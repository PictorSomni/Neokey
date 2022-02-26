# Neokey
Using Adafruit's Neokey to quickly change file names in order to sort them the way you want.
First you need to open you file explorer and navigate to a folder where you want to manually change the order of the files in it.
Touch and maintain the touchpad to activate listening mode, press the key once or several times to trigger different actions then release the touchpad to validate.

ITERATE --> :
- One press to rename the selected file and add "001" (incrementing on each file) so you can manually choose an order of files.
- 2 presses and it remove the added increment. Pay attention to what is currently selected)...
- 4 presses to close the window (ALT+F4).

COUNTER -->  :
- Maintain touch than click any times you want to increase the counter.
- When you'll let go of the touchpad, the selected file on you explorer / finder will be renamed to start with "(the number of times you clicked)X_".
- If you click the button without maintaining the touchpad,  the device will just erase the 3 first characters of the selected file, pay attention to what is currently selected)...

OLED --> :
Now a single device which makes the work of both NeoKey Trinkeys !
A feather M4 with the OLED SH1107 display and a NeoKey featherwing with 2 buttons !

Press and maintain the left button then click the right button to iterate the current selected file of your explorer / finder.
Release to confirm.

Press  and maintain the right button then click the left button several times to add the number of times you want the currently selected file to be (printed in my case).
Release to confirm.

Press both buttons to remove what you've modified using the previous commands.
