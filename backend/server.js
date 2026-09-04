import express from "express"
import dashBoardRouter from "./routes/dashBoardRouter.js"

const app = express()

app.use(express.json())

app.use("/api/dashboard", dashBoardRouter)

app.listen(3000, () => {
    console.log("Server running on port 3000")
})