const express = require('express')
const mongoose = require('mongoose')
const { spawn } = require('child_process')
const cors = require('cors')
const now = new Date();
const app = express()
app.use(express.json())
app.use(cors())

mongoose.connect('mongodb://127.0.0.1/attendance')
.then(() => console.log('Mongo connected'))
.catch(err => console.log(err))

const attendanceSchema = new mongoose.Schema({
    name: String,
    attended_time: Number,
    status: String
})


// let pythonProcess = null

// app.post('/start_attendance', (req, res) => {
//     if (pythonProcess) {
//         return res.json({ message: "Already running" })
//     }

//     console.log("START ATTENDANCE API HIT")

//     pythonProcess = spawn('python3', ['attendance_tracking.py'])

//     pythonProcess.on('close', () => {
//         console.log("Python process ended")
//         pythonProcess = null
//     })

//     pythonProcess.on('error', err => {
//         console.error(err)
//         pythonProcess = null
//     })

//     res.json({ message: "Started" })
// })

app.post('/attendance', async (req, res) => {
    date_and_time = now.toLocaleString();
    const Attendance = mongoose.model('attendance '+date_and_time, attendanceSchema)
    try {
        await Attendance.insertMany(req.body)
        res.send("Inserted")
    } catch {
        res.send("Insert error")
    }
})

app.listen(5000, () => {
    console.log('Server running on port 5000')
})
