# Daakia
Open-source e-mail backup utility from POP Servers. Bare minimum features. :envelope: :mailbox: :postbox:

![ScreenShot](https://cloud.githubusercontent.com/assets/6470801/12240596/349969f0-b8b0-11e5-928f-7cffc2fc7b6e.png)

## Installation?
LOL NO. Got Python 2 or above? You're good to go.

## Compatibility?
I have tested it on Linux and OSX, works on both. Windows etc. still need testing; there **might** be a problem of directory structures/paths which needs fixing.

## Usage?
Enter the **directory name (-d)** to save the emails in, the **URL of the POP server (-s)**, your **e-mail address (-e)** and **your password (-p)**. *Optionally*, you can also give a **(-n) number of e-mails** from the first e-mail that you want to fetch, in case you don't want to fetch all the e-mails in your inbox.
```
python daakia.py -d <folder name> -s <server name> -e <e-mail address> -p <password> [-n <integer>]
```
Example usage:
```
python daakia.py -d mails -s outlook.office365.com -e some_weirdo@lse.ac.uk -p godhelpMEe666
```
For more/better details:
```
python daakia.py --help
```
![ScreenShot](https://cloud.githubusercontent.com/assets/6470801/12240570/0c7c15bc-b8b0-11e5-9834-6045e752333d.png)

### Why the need?
I couldn't find a *free/painless* utility to download e-mails from an *Outlook Web App (OWA)* http://office365.com/owa/ account so I wrote this crude script to do the job. 

### Who will use?
A typical use case would be for backing up e-mails from expiring accounts on university/enterprise web servers. I have tried this for accounts of the following domains:
* xyz@lse.ac.uk
* abc@lums.edu.pk

### Tested?
It has been *barely tested* a couple of times for an inbox size of about 6000 mails. :neutral_face:

### Possible improvements?
This is single-threaded; downloads all e-mails serially. Will make it multi-threaded to speed things up.

### Feedback/Contact
Don't hesitate to throw in your own code or feedback on this junk.

:email: goharirfan94 [at] gmail [dot] com :neckbeard:
