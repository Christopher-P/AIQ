The Artificial Intelligence Quotient is an open source testing frameworkd used for evaluating the intelligence of an agent. We hope to further the field of AI evaluation by utilizing this framework to have a open metric for intelligence. We will also utilize this framework to determine how the field of AI is developing and whether progress towards a general intelligence being made.

# Installation
Clone this repository

# How to run

## Docker
We recommend utilizing the docker files located in this repo to run AIQ.

Navigate to the docker file, then execute the following:

```bash
docker build -t [name] .
```

this will proceed to download the required applications and python packages.

Once this is completed, run the following code to execute:

```bash
docker run [name]
```


## Stand-alone
** 3.6.6 **

To run this without utilizing the docker system, follow the download
instructions for the following packages:

[keras](https://github.com/keras-team/keras)

[tensorflow](https://github.com/tensorflow/tensorflow)

[gym+gym[atari]](https://github.com/openai/gym)

[vizdoom](https://github.com/mwydmuch/ViZDoom)

Specifics can be found inside the Dockerfile inside the docker directory.

# Results
Results can be submitted to our website to be logged and displayed on a public leaderboard!
Visit the [AIQ Website](https://portal.eecs.wsu.edu/aiq/).


# Citations
ViZDoom:
Michał Kempka, Marek Wydmuch, Grzegorz Runc, Jakub Toczek & Wojciech Jaśkowski, ViZDoom: A Doom-based AI Research Platform for Visual Reinforcement Learning, IEEE Conference on Computational Intelligence and Games, pp. 341-348, Santorini, Greece, 2016	(arXiv:1605.02097)

AI2: 
http://data.allenai.org/arc/

OpenAIGym:
@misc{1606.01540,
  Author = {Greg Brockman and Vicki Cheung and Ludwig Pettersson and Jonas Schneider and John Schulman and Jie Tang and Wojciech Zaremba},
  Title = {OpenAI Gym},
  Year = {2016},
  Eprint = {arXiv:1606.01540},
}







