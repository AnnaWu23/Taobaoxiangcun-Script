# Taobao Seckill Assistant

[English](README.md) | [中文](README.zh.md)

## Technical Highlights

### 1. Core Technical Implementation
- **Complete Automation Process**
  - Multi-threaded concurrent processing
  - Precise timing control
  - Automatic error recovery
  - Request frequency optimization

- **Stable Network Request Handling**
  - Proxy server support
  - Cookie persistence management
  - Request retry mechanism
  - Network exception handling

- **User-friendly Interface**
  - Real-time status updates
  - Intuitive operation flow
  - Clear error prompts
  - Responsive design

### 2. Code Quality
- **Modular Design**
  - Clear module boundaries
  - High cohesion, low coupling
  - Easy to maintain and extend
  - Reusable components

- **Clear Code Structure**
  - Standardized naming conventions
  - Logical code organization
  - Clean code practices
  - Efficient algorithms

- **Comprehensive Documentation**
  - Detailed code comments
  - API documentation
  - Usage guides
  - Development notes

## Project Overview

This is a Python-based automated tool for Taobao seckill, designed to improve efficiency in purchasing limited-time offers on Taobao platform. The project features a modular design, complete graphical user interface, support for multiple product purchases, and comprehensive product management capabilities.

## Technical Architecture

### Core Framework
- Python 3.7+
- Tkinter (GUI Framework)
- Selenium (Web Automation)
- mitmproxy (Network Request Proxy)

### Data Processing
- requests (HTTP Request Handling)
- pickle (Data Serialization)
- xlrd/openpyxl (Excel File Processing)
- LocalDatabase (Local Data Storage)

### Network Communication
- Asynchronous Request Processing
- Cookie Management
- Proxy Server Support

## Features

### 1. User Interface
- Intuitive Graphical Interface
- Product List Management
- Real-time Status Display
- Operation Log Recording

### 2. Product Management
- Multiple Product Purchase
- Product Information Import/Export
- Price Monitoring
- Stock Monitoring

### 3. Account Management
- Automatic Login
- Cookie Persistence
- Multiple Account Support

### 4. Purchase Features
- Scheduled Purchase
- Shopping Cart Management
- Automatic Order Placement
- Order Status Tracking

## Project Structure

```
Taobaoxiangcun-Script/
├── 淘宝秒杀 - 第一代/    # Initial Version
├── 淘宝秒杀 - 第二代/    # Optimized Version
├── 淘宝秒杀 - 第三代/    # Latest Stable Version
├── 讨论文件/            # Development Documents
└── revising/           # New Features in Development
```

## Installation & Deployment

### Environment Requirements
- Python 3.7+
- Chrome Browser
- ChromeDriver (Matching Chrome Version)

### Installation Steps
1. Clone the Project
```bash
git clone [project-url]
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Configure ChromeDriver
- Download matching ChromeDriver version
- Add ChromeDriver to system PATH

## User Guide

### First-time Use
1. Run the Program
```bash
python class_win.py
```

2. Login to Taobao
- Click Login Button
- Scan QR Code to Complete Login

3. Add Products
- Input Product URL
- Set Purchase Time
- Save Product Information

### Daily Use
1. Start the Program
2. Select Products to Purchase
3. Set Purchase Time
4. Click Start Seckill

## Development History

### First Generation
- Basic Function Implementation
- Single Product Purchase
- Simple GUI Interface

### Second Generation
- Multiple Product Support
- Performance Optimization
- Interface Enhancement

### Third Generation
- Complete Function Implementation
- Stability Improvement
- User Experience Optimization

## Technical Challenges

1. Network Request Handling
- Request Frequency Control
- Proxy Server Configuration
- Cookie Management

2. Interface Interaction
- Real-time Status Updates
- Multi-threading Processing
- Exception Handling

3. Data Management
- Local Data Storage
- Product Information Synchronization
- Order Status Tracking

## Future Plans

1. Function Optimization
- Intelligent Purchase Strategy
- Price Prediction
- Stock Monitoring

2. Performance Improvement
- Concurrency Optimization
- Memory Management
- Response Speed Enhancement

3. User Experience
- Interface Beautification
- Operation Simplification
- Error Message Optimization

## Notes

1. Usage Guidelines
- Follow Taobao Platform Rules
- Set Reasonable Purchase Frequency
- Pay Attention to Account Security

2. Technical Limitations
- Network Environment Dependency
- Chrome Browser Required
- Platform Update Risks

## Disclaimer

This project is for learning and communication purposes only. Please do not use it for commercial purposes. The developer is not responsible for any issues arising from the use of this tool. 