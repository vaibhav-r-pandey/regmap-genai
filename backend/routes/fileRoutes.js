const express = require("express");
const FileData = require("../models/FileData");
const router = express.Router();

router.post("/", async (req, res) => {
  try {
    const { text1, text2, differences } = req.body;
    const newFileData = new FileData({ text1, text2, differences });
    await newFileData.save();
    res.status(201).json({ message: "Comparison data saved successfully" });
  } catch (error) {
    res.status(500).json({ message: "Error saving data", error });
  }
});

module.exports = router;
