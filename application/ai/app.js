const express = require('express');
const cors = require("cors");
require("dotenv").config();

const llmRoutes = require('./routes/llm.routes');

const app = express();

app.use(express.json());
app.use(cors());

app.use('/llm', llmRoutes);

app.get('/', (req, res) => {
  res.send('API LLM está rodando!');
});

module.exports = app;
