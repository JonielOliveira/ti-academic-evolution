const { extractKeywords } = require('../services/llm.service');

/**
 * Controller que processa a extração de palavras-chave.
 *
 * @param {Request} req
 * @param {Response} res
 */
async function extractKeywordsController(req, res) {
  const { title, abstract } = req.body;

  if (!title || !abstract) {
    return res.status(400).json({ error: 'Campos "title" e "abstract" são obrigatórios.' });
  }

  try {
    const keywords = await extractKeywords(title, abstract);
    return res.status(200).json({ keywords });
  } catch (error) {
    console.error('Erro ao consultar o LLM::', error.message);
    return res.status(500).json({ error: 'Erro ao processar a extração de palavras-chave.', details: error.message });
  }
}

module.exports = {
  extractKeywordsController
};
