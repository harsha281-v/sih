import { Router } from "express"

const dashBoardRouter = Router()

dashBoardRouter.get("/overview", (req, res) => {
    const data = {
        name: "Virat",
        age: 30
    }

    res.status(200).json({success: true, data})
})

dashBoardRouter.get("/forecast", (req, res) => {
    const data = {
        current_attack_type: "fast",
        current_attack_probability:0.78,
        future_attack_type: "fast",
        future_attack_probability:0.78
    }

    res.status(200).json({
        success: true,
        data
    })
})

export default dashBoardRouter