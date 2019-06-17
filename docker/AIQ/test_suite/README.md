# Adding a test to AIQ

## Active Environments

### Requirements

Active Environments assume a constant interaction between the environment and the agent during the evaluation phase. For a test to be an active environment, it must meet the following requiremtents:

1. Have a well-defined and consistent input and output space.

2. Accept a well-defined action to then return an observation and reward.

3. Have a finite runtime and return a completion flag along with a final score.

### Adding the test

To add a singular active environment to AIQ follow these steps:

1. Create a file with the test name in the test_suite.

2. Create a class with the same name in that file.

3. Inherit from the common descriptor class and header class (for universality).

4. Define the header. The header contains useful universal information for all environments in the AIQ framework.

  * Define the environment name.
  * Define input and output spaces.
  * Give environment information.
  * Set min/max final scores.


5. Implement the act function.

  * Must accept an action according to the defined input space.
  * Map the action to the environment's input (variable).
  * Move the environment forward a step according to the input.
  * Return the current state of the environment and step-wise reward.
  * Current state must follow the defined output space.

6. Implement the reset function.

  * Must be callable at any point.
  * Must fully reset the environment according to its initial conditions.
  * Must make the environment fully ready for an action to be sent.
  * Return the initial state of the environment.

7. Implement additional functions.

  * Additional functions may be implemented according to the specifics of the environment.
  * If the environment supports visualization then implement the render function.


### Adding a test set

1. Expect 'env_name' to be in sent params.

2. From this string, pull the specific subtest from the set according to the set's implementaiton.

* The AIQ framework works by handling many individual tests, the subtest must be one well defined test!

3. Follow the steps for adding an active environment, but they must be made generalizable to all tests in the set (see openaigym for example).

### Adding additional external data

If the test requires additional external data follow this steps to add it:

1. Make a directory in the test_suite folder with the data.

It is preffered to have the directory reference within the test file, but it may also be passed as a parameter.

2. By default have the data location within the test file

3. Allow for 'config' param to overwrite the location of the data directory.

## Passive Environments

### Requirements

Passive environments assume a singular interaction between the environment and the agent during the evaluation phase. For a test to be an assive environment, it must meet the following requiremtents:

1. Have a well-defined and consistent input and output space.

2. Accept a well-defined response to then return a score.

3. Fully present all data when requested.

### Adding a test

1. Create a file with the test name in the test_suite.

2. Create a class with the same name in that file.

3. Inherit from the common descriptor class and header class (for universality).

4. Define the header. The header contains useful universal information for all environments in the AIQ framework.

  * Define the environment name.
  * Define input and output spaces.
  * Give environment information.
  * Set min/max scores.

5. Implement the get_test function.

  * Must return a set of problems according to the output space.

6. Implement the evaluate function.

  * Must accept a set of solutions according to the input space.
  * Must return a score for the solutions according to the problems generated in get_test.

7. Additional functions.

  * It is strongly recommended to implement the get_train function. This function will provide both a set of problems and a set of solutions. Scoring and training will be left to the agent.
  * It is recommended to implement the get_dev function. This can be used to evaluate the agent on unseen data without exposing it to the test data.
  * Any test specific functions should be added (complicated scoring functions, rendering, remote calls)

## Adding a test set

  1. Expect 'env_name' to be in sent params.

  2. From this string, pull the specific subtest from the set according to the set's implementaiton.

  * The AIQ framework works by handling many individual tests, the subtest must be one well defined test!

  3. Follow the steps for adding an environment, but they must be made generalizable to all tests in the set (see openaigym for example).

## Adding additional external data

  If the test requires additional external data follow this steps to add it:

  1. Make a directory in the test_suite folder with the data.

  It is preffered to have the directory reference within the test file, but it may also be passed as a parameter.

  2. By default have the data location within the test file

  3. Allow for 'config' param to overwrite the location of the data directory.
