# AI-Powered-Web-Shooting-My-Agentic-AI-Project
🕷️ AI Gesture-Controlled Web Shooting System

A real-time computer vision project that transforms hand gestures into cinematic web-shooting actions.

The system uses MediaPipe's pretrained ML-based Hand Landmarker for real-time hand tracking, custom gesture recognition, and an agent-based decision layer to trigger web-shooting actions with visual effects, voice feedback, and sound effects.

---

## 🚀 Project Overview

This project creates an interactive AR-like experience where a user can perform a specific Spider-Man-inspired hand gesture in front of a webcam.

When the gesture is detected and validated, the system processes the gesture through an agent-based decision layer and triggers:

- 🖐️ Real-time hand landmark detection
- 🕷️ Custom web-shoot gesture recognition
- 🤖 Agent-based action decision
- 🎬 Cinematic web-shooting VFX
- 🎯 Screen-targeted web effect
- 🔊 Web-shooting sound effect
- 🗣️ AI voice feedback
- ⏱️ Gesture cooldown mechanism

---

## ✨ Key Features

### 1. Real-Time Hand Tracking

The system uses MediaPipe Hand Landmarker to detect hand landmarks from the webcam in real time.

The detected landmarks are used as the foundation for gesture recognition.

### 2. Custom Gesture Recognition

A Spider-Man-inspired gesture is identified by checking the relative positions of specific finger landmarks.

The gesture uses:

- Index finger → Up
- Middle finger → Down
- Ring finger → Down
- Little finger → Up

This combination triggers the web-shoot gesture.

### 3. Gesture Stability Detection

The system does not immediately trigger the action from a single frame.

The detected gesture must remain stable for a short period before the action is processed.

This helps reduce accidental triggers caused by temporary hand movements.

### 4. Agent-Based Decision Layer

After gesture detection, the event is passed to a custom agent decision engine.

The agent determines whether the action should be:

- `WEB_SHOOT`
- `IDLE`
- `IGNORE`
- `COOLDOWN`
- `UNKNOWN`

Only an approved `WEB_SHOOT` decision triggers the shooting effect.

### 5. Cinematic Web VFX

The project includes a custom transparent web effect designed to appear as a shooting web rather than a continuously displayed overlay.

The effect includes:

- Multiple web strands
- Curved motion
- Glow
- Web head
- Impact rings
- Impact strands
- Animated shooting motion

### 6. Screen Targeting

A laptop screen can be calibrated using four screen corner points.

The detected hand position is then used to determine the target area for the web effect.

### 7. Voice Feedback

The system provides voice feedback for meaningful AI/agent events using text-to-speech.

This makes the interaction more immersive and gives audio feedback when the system processes an action.

### 8. Sound Effects

A web-shooting sound effect is triggered when the agent approves a web-shoot action.

The project uses an original/generated sound effect rather than copyrighted movie audio.

### 9. Cooldown Mechanism

A cooldown is implemented between web-shoot actions to prevent the same gesture from triggering the effect repeatedly in rapid succession.

---

## 🧠 AI / ML Component

The AI/ML component of this project comes from MediaPipe's pretrained Hand Landmarker model.

It performs machine-learning-based hand landmark detection from the webcam feed.

On top of this ML-based perception layer, the project implements:

1. Custom rule-based gesture recognition
2. Gesture stability validation
3. Agent-based decision logic
4. Action execution

The project does not use a separately trained custom ML model or an LLM.

---

## 🏗️ System Architecture


              Webcam
                 │
                 ▼
             OpenCV
                 │
                 ▼
       MediaPipe Hand Landmarker
                 │
                 ▼
       Hand Landmark Detection
                 │
                 ▼
    Custom Gesture Recognition
                 │
                 ▼
      Gesture Stability Check
                 │
                 ▼
       Agent Decision Engine
                 │
          ┌──────┴──────┐
          │             │
       Execute         Ignore
          │
          ▼
     Action Execution
          │
    ┌─────┼─────┐
    │     │     │
    ▼     ▼     ▼
   VFX   Sound  Voice
    │
    ▼
 Screen-Targeted
 Web Effect
