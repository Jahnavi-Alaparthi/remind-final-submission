# Remind :An Agentic AI tutor for memory retention  
*A Socratic Tutor with Spaced Repetition*

##  Introduction
The **Remind Project** is a learning support system that combines a **Socratic-style tutor** with a **spaced repetition reminder mechanism**.  
Its main goal is to help users retain knowledge effectively by deciding *what* to revise and *when* to revise it.

Instead of repeatedly revising all questions, the system adapts based on how well the user remembers each question.

---

##  Objectives
- Engage users through guided, Socratic-style questioning
- Store previously asked questions persistently
- Track learning progress using levels and memory-related factors
- Schedule intelligent reviews using spaced repetition principles

---

##  Technologies Used
- Python
- JSON for persistent storage
- Date and Time handling
- Logical scheduling algorithms

---

---

##  Learning Approach
The project is based on **spaced repetition**, a scientifically proven learning technique where revision intervals increase as memory strengthens.  
Difficult or newly learned questions are reviewed more frequently, while well-known questions appear less often.

---



## Socratic Chatbot: Socratic Tutor and Question Logging Module

**Purpose:**  
This module initiates the learning process by interacting with the user in a **Socratic manner** while recording the question for future review.

**Functionality:**  
- Accepts a question from the user  
- Responds using guided explanations or probing prompts  
- Encourages reasoning instead of directly giving answers  
- Stores the question along with the time it was asked

**Why Socratic:**  
Rather than acting as a simple answer bot, this module:
- Promotes active thinking  
- Helps users understand *how* concepts work  
- Builds conceptual clarity

**Role in the system:**  
Module Socratic tutor acts as the **entry point**, passing stored questions to later modules for evaluation and scheduling.

---

## SpacedChatbot: Learning Level Assignment Module

**Purpose:**  
To measure how well the user understands a particular question.

**How it works:**  
- Each question is assigned a **learning level**
- Levels increase when the user recalls or understands the concept successfully
- Lower levels indicate weak or new understanding

**Why levels matter:**  
The learning level directly affects:
- Review frequency  
- Memory strength calculation  
- Forgetting speed estimation

This module creates a structured representation of user mastery.

---

## Advanced chatbot : Review Scheduling Using Memory Factors

**Purpose:**  
To determine **which questions are due for review** at a given time using memory-related parameters.

**Key Factors Used:**

### 1. Difficulty
- Represents how hard a question is for the user
- Difficult questions require more frequent revision
- Difficulty is inferred from low learning levels or repeated failures

### 2. Forgetting Speed
- Models how quickly a user is likely to forget a question
- Higher forgetting speed → shorter revision intervals
- Lower forgetting speed → longer gaps between reviews

### 3. Memory Strength
- Indicates how firmly a concept is stored in memory
- Increases as the user successfully reviews the question
- Strong memory allows the system to delay the next review

**How scheduling works:**  
The system checks:
- The last reviewed time
- Learning level
- Difficulty
- Forgetting speed
- Memory strength

Using these factors, it calculates whether a question is **eligible for review at the current time**.

**Why this approach is effective:**  
This prevents unnecessary repetition and ensures that attention is focused on concepts the user is most likely to forget.

---

##  Advantages of the System
- Personalized learning experience
- Efficient use of revision time
- Encourages deeper understanding
- Scalable and modular design

---

##  Future Enhancements
- User interface integration
- Multi-user support
- Performance analytics dashboard
- Notifications and reminders

---

## 👤 Author
**Jahnavi Alaparthi**

---

##  Conclusion
The Remind Project demonstrates how educational psychology concepts such as the Socratic method and spaced repetition can be translated into a practical software system.  
By combining guided learning with adaptive review scheduling, the project creates an effective and intelligent revision workflow.


