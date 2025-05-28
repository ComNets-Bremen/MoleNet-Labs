# MoleNet Labs

This repository contains lab materials developed for the **MoleNet** development board. These labs are designed to teach students and developers about embedded wireless communication, energy-aware programming, and protocol implementation using popular toolchains like Arduino and MicroPython.

Each lab focuses on a different topic and includes slides, sample code, and evaluation material.

---

## 📁 Repository Structure

The repository is organized into folders by lab. Each lab folder typically contains:

- `slides/` – Presentation material used during the lab session. Introduction to IDEs or other hardware used in specific lab
- `code_template/` – Sample or starter code to be used on MoleNet. Provides supporting libraries required for the lab
- `evaluation/` – Evaluation instructions, checklists, or assignment sheets
- `manual/` - The PDF file of the exercise
- `server/receiver` - Code for the server or the receiver that needs to be setup for the respective lab

---

## 🧪 Available Labs

### 🔹 Lab 1 – WiFi Communication with Arduino

**Topic:** UDP and TCP communication using MoleNet over WiFi  
**Tools:** Arduino IDE, ESP8266/ESP32 (via MoleNet)  
**Skills Learned:**
- Setting up WiFi on embedded systems
- Sending and receiving UDP and TCP packets
- Debugging network issues

📂 Navigate to: `arduino-wlan-lab/`

---

### 🔹 Lab 2 – LoRa Communication with MicroPython

**Topic:** Long-range communication using LoRa protocol  
**Tools:** MicroPython, MoleNet with LoRa module  
**Skills Learned:**
- Writing MicroPython scripts for LoRa
- Sending sensor data over LoRa
- Understanding LoRa communication for point to point communication

📂 Navigate to: `micropython-energy-lab/`

---

### 🔹 Lab 3 – Energy Consumption with MicroPython

**Topic:** Measuring and optimizing energy consumption on embedded systems  
**Tools:** MicroPython, USB power meter  
**Skills Learned:**
- Understanding power profiles of different communication protocols
- Building energy model to estimate the energy consumption of the board
- Comparing theoretical and practical values for energy consumption

📂 Navigate to: `micropython-lora-lab/`

---
