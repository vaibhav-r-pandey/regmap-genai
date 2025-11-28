const mongoose = require("mongoose");

const FileDataSchema = new mongoose.Schema({
  text1: { type: String, required: true },
  text2: { type: String, required: true },
  differences: { type: Array, required: true },
});

module.exports = mongoose.model("FileData", FileDataSchema);