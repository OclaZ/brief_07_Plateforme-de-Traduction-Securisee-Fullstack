'use client';

import { useState } from 'react';
import { Loader2, Languages, ArrowLeftRight } from 'lucide-react';

export default function TranslatePage() {
  const [text, setText] = useState('');
  const [direction, setDirection] = useState('en_fr');
  const [translation, setTranslation] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleTranslate = async (e) => {
    e.preventDefault();
    
    if (!text.trim()) {
      setError('Le texte ne peut pas être vide');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess(false);
    setTranslation('');

    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        setError('Vous devez être connecté pour utiliser la traduction');
        setLoading(false);
        return;
      }

      const response = await fetch('http://localhost:8000/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text: text,
          direction: direction
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Erreur lors de la traduction');
      }

      // Extract translation from nested response structure
      const translatedText = data.traduction?.[0]?.[0]?.translation_text || 
                           data.traduction?.[0]?.translation_text || 
                           'Traduction non disponible';
      
      setTranslation(translatedText);
      setSuccess(true);

    } catch (err) {
      setError(err.message || 'Une erreur est survenue');
    } finally {
      setLoading(false);
    }
  };

  const toggleDirection = () => {
    setDirection(prev => prev === 'en_fr' ? 'fr_en' : 'en_fr');
    setTranslation('');
    setSuccess(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Header */}
          <div className="flex items-center justify-center mb-8">
            <Languages className="w-10 h-10 text-indigo-600 mr-3" />
            <h1 className="text-3xl font-bold text-gray-800">Traduction</h1>
          </div>

          {/* Form */}
          <div className="space-y-6">
            {/* Language Direction Selector */}
            <div className="flex items-center justify-center space-x-4">
              <div className="flex items-center space-x-2">
                <span className={`px-4 py-2 rounded-lg font-semibold ${
                  direction === 'en_fr' 
                    ? 'bg-indigo-600 text-white' 
                    : 'bg-gray-100 text-gray-700'
                }`}>
                  {direction === 'en_fr' ? 'EN' : 'FR'}
                </span>
                
                <button
                  type="button"
                  onClick={toggleDirection}
                  className="p-2 rounded-full hover:bg-gray-100 transition-colors"
                  title="Inverser la direction"
                >
                  <ArrowLeftRight className="w-6 h-6 text-gray-600" />
                </button>

                <span className={`px-4 py-2 rounded-lg font-semibold ${
                  direction === 'fr_en' 
                    ? 'bg-indigo-600 text-white' 
                    : 'bg-gray-100 text-gray-700'
                }`}>
                  {direction === 'en_fr' ? 'FR' : 'EN'}
                </span>
              </div>
            </div>

            {/* Text Input */}
            <div>
              <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
                Texte à traduire
              </label>
              <textarea
                id="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder={direction === 'en_fr' 
                  ? 'Enter your text in English...' 
                  : 'Entrez votre texte en français...'}
                rows={6}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                disabled={loading}
              />
            </div>

            {/* Submit Button */}
            <button
              onClick={handleTranslate}
              disabled={loading || !text.trim()}
              className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Traduction en cours...
                </>
              ) : (
                'Traduire'
              )}
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800 text-sm font-medium">{error}</p>
            </div>
          )}

          {/* Success Result */}
          {success && translation && (
            <div className="mt-6 p-6 bg-green-50 border border-green-200 rounded-lg">
              <h3 className="text-lg font-semibold text-green-900 mb-3">
                Traduction réussie
              </h3>
              <div className="bg-white p-4 rounded-lg border border-green-100">
                <p className="text-gray-800 whitespace-pre-wrap">{translation}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}