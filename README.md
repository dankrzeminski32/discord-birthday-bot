# BirthdayDiscordBot 🎂

A simple and easy to use Birthday Discord Bot which helps to boost server comradery and friendship. 

## Description

Simply add the bot to your server and have each user register with the ```.bday register``` command.

Every 24 hours the bot will send out a special announcement for any registered users with a birthday on that day.

## Getting Started

### Executing program

**1.)** - Create a Virtual Environment

```bash
python3 -m venv venv
```

**2.)** - Activate this Environment,

```bash
cd venv
```

```bash
source bin/activate
```

**3.)** - Install requirements.txt (Make sure you are in project root)

```bash
pip install -r requirements.txt
```

**4.)** - Run the bot

```bash
python run.py
```

### Black Formatting

There is a github action for this repository that runs with every pull request.

This action checks to make sure that you properly formatted your changes with the Python [black formatter](https://black.readthedocs.io/en/stable/)

To pass this check, run the black formatter across the entire project after your last commit.

**As shown below,**

**1.)** - Make sure black is installed

```bash
pip install black
```

**2.)** - Format the entire project (make sure you are in root directory)

```bash
black .
```

**3.)** - Add the formatted files

```git
git add .
```

**4.)** - Push the formatted files

```git
git commit -m "black formatting"
git push
```

## Authors

Daniel Krzeminski - dankrzeminski32@gmail.com

Ethan Kvachkoff

## Version History

Yet to be established

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
