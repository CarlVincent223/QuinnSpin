🧺 QuinnSpin  
A Mobile & Desktop Laundry Service Management System for Quinn's Laundry House

QuinnSpin is an integrated *mobile*, *desktop*, and *cloud-based* application designed to streamline the operations of Quinn’s Laundry House in Naga City.  
It replaces manual booking, inefficient communication, and paper-based tracking with a modern, real-time digital system.

---

🚀 Features

👤 Customer Mobile App
- Online booking with service details and special instructions  
- Real-time order tracking (Pending → Confirmed → Pickup → Processing → Delivery → Completed)  
- Push notifications via Firebase Cloud Messaging  
- Loyalty points with gamified rewards  
- Digital payment status & order history  
- Profile management  

🧑‍💼 Admin Desktop App
- Booking management and rider assignment  
- Payment status update and invoice generation  
- Customer account management  
- Sales analytics and reports (Excel & PDF)  
- Service and pricing configuration  
- In-app customer messaging  
- Rider performance tracking  

🚴 Rider Mobile App
- Task notifications for pickup & delivery  
- Real-time task confirmation (Start → Complete)  
- Access to customer details & instructions  
- Task history and performance stats  

---

🏗️ System Architecture

QuinnSpin is built using a multi-application architecture:

| Component | Technology |
|----------|------------|
| *Customer App* | Solar2D + Lua |
| *Rider App* | Solar2D + Lua |
| *Admin App* | Python + Tkinter |
| *Backend API* | Flask (Python) |
| *Database* | PostgreSQL |
| *Push Notifications* | Firebase Cloud Messaging |
| *Hosting* | Render.com (Cloud Server) |

---

📊 Performance Benchmarks

| Metric | Target | Actual |
|--------|--------|--------|
| Page Load Time | ≤ 3 sec | *2 sec* |
| Notification Delivery | ≤ 5 sec | *3 sec* |
| API Response Time | ≤ 500 ms | *310 ms* |
| Database Write | ≤ 1 sec | *0.4 sec* |
| Database Read | ≤ 1.5 sec | *0.7 sec* |
| Concurrent Users | ≥ 100 | *100+ stable* |
| Server Uptime | ≥ 99% | *99.5%* |

---

🧩 Key Modules

- *Booking & Scheduling*
- *Order Tracking*
- *Loyalty & Rewards*
- *Billing & Payment Tracking*
- *Sales Reporting*
- *User & Role Management*
- *Rider Dispatching*

---
