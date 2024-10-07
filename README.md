# EcoTrack
A Smart Waste Segregation and Recycling Management Platform

![WhatsApp Image 2024-09-09 at 18 50 53_b79c9a65](https://github.com/user-attachments/assets/54b71ae0-fd3d-453b-a943-800cd4a7eacc)

This project implements a basic Waste Segregation and Recycling Management System (WSRMS). The system aims to efficiently manage waste information, user data, and recycling notifications.
System Overview

https://youtu.be/76pSwdEtiqY -->Demo 

# The WSRMS consists of the following key components:
 
    User Registration and Authentication
    Waste Information Database
    User Data Entry for Waste Management
    Distance-based Recycler Notification System
    Confirmation Email System
    Gamification -Reward System

# Workflow

Users register and authenticate to access the system.
Authenticated users can enter waste management data into the system.
The system stores waste information in a database.
A decision process checks if the distance between the waste location and the nearest recycler is less than a specified threshold.
If the distance criteria are met, the system sends a notification (presumably to the recycler or relevant authorities).
After processing, the system sends a confirmation email about the ready-to-collect waste.
Emails are sent using the SMTP protocol.

This system aims to streamline waste management processes, improve recycling efficiency, and facilitate communication between waste producers and recyclers.

# Technologies Used

Database management for waste information storage
User authentication system
SMTP protocol for email communications
Distance calculation algorithms (for determining proximity to recyclers)
