const express = require('express');
const router = express.Router();

const { extractKeywordsController } = require('../controllers/llm.controller');

router.post('/extract-keywords', extractKeywordsController);

module.exports = router;
