# Project Using the W5100S-EVB-PICO Board - Translating Visuals into Words: Image Captioning with AI

## Overview

In this project, we are using two W5100S-EVB-PICO boards.

1.The first board connects an Arducam and Ethernet to serve the role of transmitting a picture to a web page upon receiving a web request.

![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-ImageCaptioning/assets/115054808/d8921838-cfed-4157-ab0b-ed93ded69172)

2.The second board will perform image-to-text captioning via the "Replicate API" in the form of a web address serving images from the first PICO board over an Ethernet connection and display them on the ssd1306 OLED screen.

![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-ImageCaptioning/assets/115054808/71c9cca9-484c-4927-896a-577ff6c80bb8)


Discuss this in more detail below.

## Model used for image captioning 

BLIP-2 is a part of Salesforce's LAVIS project. BLIP-2 is a generic and efficient pre-training strategy that leverages the advancements of pretrained vision models and large language models (LLMs). BLIP-2 surpasses Flamingo in zero-shot VQAv2 (scoring 65.0 vs 56.3) and sets a new state-of-the-art in zero-shot captioning (achieving a CIDEr score of 121.6 on NoCaps compared to the previous best of 113.2). When paired with powerful LLMs such as OPT and FlanT5, BLIP-2 unveils new zero-shot instructed vision-to-language generation capabilities for a range of intriguing applications.

![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-ImageCaptioning/assets/115054808/424c38c5-62f4-48fb-8cbc-565dfafbcffe)

[Model testable on Replicate](https://replicate.com/andreasjansson/blip-2)

![image](https://github.com/dbtjr1103/W5100S-EVB-PICO-ImageCaptioning/assets/115054808/8bd98582-f653-4169-8124-f485d8cdfb1d)

[Research paper on the model](https://arxiv.org/abs/2301.12597)

[Official GitHub](https://github.com/salesforce/LAVIS/tree/main/projects/blip2)
  

## Installation Guide

Steps to install and set up this project on a local environment:

1. Install necessary libraries and dependencies.
2. Set up and connect the W5100S-EVB-PICO board.


## How to Use

1. Connect and configure the Arducam.
2. Set up the Ethernet connection.
3. Communicate between the PICO board and web server.
4. View results and display captions.

## Demos and Outputs

Links to demonstrations and examples of project results:

- [Demo Video Link](#)
- Screenshots and case examples of results.

  
## Potential Developments

The current focus of this project is on captioning an image and displaying the text. However, by adding speakers in the future, this could evolve into applications for the visually impaired or anomaly detection, among various other project ideas.

## Contributions and Feedback

Contributions and feedback on the project are always welcome. Please use the GitHub issue tracker to report issues or create pull requests.
