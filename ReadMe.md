
# Association Rule Mining using Apriori

Apriori is a classical algorithm for mining association rules. This code for mining association rules using Apriori algorithm is written in Python 3.

# How to run the code:

(1) First, download and unzipped the folder and enter that folder. Then run the following command from a terminal to run the code: (Required dataset 'Play_Tennis_Data_Set.csv' should be in the same folder)

    $ python3 AprioriRuleMining.py

(2) After running the program, you will see the following user prompt to enter minimum support and minimum confidence one at a time.

    Enter the minimum support (fraction value): 
    Enter the minimum confidence (fraction value): 

(3) Here, user input for both minimum support and minimum confidence are fraction value. For example, if we enter '0.3' as minimum support and '0.6' as minimum confidence and then press Enter key on the keyboard, then mined association rules from dataset will be displayed like below:

    User Input:

     Support: 0.3
     Confidence: 0.6

    Rules:

     Rule#1: {PlayTennis=P} => {Windy=FALSE}
     (Support=0.43, Confidence=0.67)

     Rule#2: {Windy=FALSE} => {PlayTennis=P}
     (Support=0.43, Confidence=0.75)

     Rule#3: {PlayTennis=P} => {Humidity=normal}
     (Support=0.43, Confidence=0.67)

     Rule#4: {Humidity=normal} => {PlayTennis=P}
     (Support=0.43, Confidence=0.86)

   Thank you!

# Contact:
Md. Mahbub Alam (emahbub.cse@gmail.com)
