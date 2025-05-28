const axios = require('axios');
require("dotenv").config();

const LLM_URL = process.env.LLM_URL;
const MODEL = process.env.LLM_MODEL;

/**
 * Gera palavras-chave a partir de título e resumo de um documento acadêmico.
 *
 * @param {string} title - O título do documento.
 * @param {string} abstract - O resumo do documento.
 * @returns {Promise<string[]>} - Array com 3 palavras-chave.
 */
async function extractKeywords(title, abstract) {
  const prompt = `
A seguir está o título e o resumo de um documento acadêmico. 
Baseado nisso, extraia e retorne apenas 3 palavras-chave que melhor representam o conteúdo.

Título: ${title}

Resumo: ${abstract}

Responda apenas com as palavras-chave separadas por vírgula.
`;

  try {
    const response = await axios.post(LLM_URL, {
      model: MODEL,
      prompt: prompt,
      stream: false
    });

    const reply = response.data.response.trim();

    console.log('Resposta do LLM:', reply);

    // Converte a resposta em array
    const keywords = reply.split(',').map(k => k.trim()).filter(k => k.length > 0);

    return keywords.slice(0, 3); // Garante no máximo 3
  } catch (error) {
    console.error('Erro ao consultar o LLM:', error.message);
    throw error;
  }
}

module.exports = { extractKeywords };
