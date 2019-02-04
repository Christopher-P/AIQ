The Artificial Intelligence Quotient is an open source testing frameworkd used for evaluating the intelligence of an agent. We hope to further the field of AI evaluation by utilizing this framework to have a open metric for intelligence. We will also utilize this framework to determine how the field of AI is developing and whether progress towards a general intelligence being made.

# Installation
Clone this repository

PyPi Coming soon!

# How to run

1. Follow Tutorial
2. Build with Docker


## Tutorial

1. To begin rename sample.yml located in the docker to credentials.yml and
put in your username and password. 

2. Import the AIQ interface
```python
import AIQ
```


3. Send login information to the interface
```python
interface = AIQ(username, password)
```
Dummy information can be passed instead to utilize AIQ locally only.
Remove any references to connection and submission.

4. Verify credentials work
This is sent via a secure connection but we are still working on sending fully encrypted data.
```python
# returns True if credentials match our system
interface.connect()
```

5. Add tests to test suite
  * Simple Test
```python
interface.add('[name]')
```

  * Subtest in package
```python
# Example: [package] = OpenAIGym, [subtest] = CartPole-v0
interface.add('[package]', {'env_name':'[subtest]'})
```

  * Subtest in package with parameters
```python
# Example: [package] = VizDoom, [subtest] = basic
    params = {}
    params['config'] = "path_to_config"
    params['subtest'] = [subtest]
    interface.add('[package]', params=params)
```


6. Add an agent
AIQ provides an agent which randomly selects from the possible actions given
by the test with knowledge of each test.
```python
from AIQ.agents.random_agent import R_Agent
interface.agent = R_Agent()
```


7. Evaluate the agent on the test suite
```python
interface.evaluate()
```


8. The results can then be seen and submitted to the AIQ leaderboard.

This will result in an unvalidated but public score. We are currently working on
creating a submission process to verify each submission.

```python
# Print results (dictionary) from evaluation
print(interface.results)

# Submit and print server feedback
print(interface.submit())
```

9. All of this can be found within the full_test file inside the examples directory.

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
