# PythonGraphDraw
Prompts participants to trace a set of line graphs, calculates how close the drawing was, and sends this data to Unreal4 and starts up the linked task.

# Overview
This task has a set of predefined graphs that are drawn to the screen using the TKinter library. The participant must then trace each of these tasks with their mouse. Once the trace is complete how close the trace was is calculated by using Max Bareiss's implementation of the weak Frechet distance algorithm here: https://gist.github.com/MaxBareiss/ba2f9441d9455b56fbc9

This data is then passed to Unreal 4 via the command line with the participant's name. The game starts up and the player's proceed to complete their tasks and have their previous tracing data submitted to Google forms with the rest of the data.
