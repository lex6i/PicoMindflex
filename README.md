# PicoMindflex
A port of https://github.com/kitschpatrol/Brain for the Raspberry pico

Hardware instructions can be found [here]([https://link-url-here.org](https://rootsaid.com/getting-raw-data-mindflex-using-arduino/))


usage example sending

    from mindflex import MindFlex
    
    m = MindFlex()
    
    while True:
        m.readPacket()
        if m.freshPacket:
            o = m.readCSV()
            print(o)

## todo
* Increase stability, it tends to crash
