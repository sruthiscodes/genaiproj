import React, { useState, useEffect, useRef } from 'react';
import { Send, RefreshCw, Heart } from 'lucide-react';

const GameService = {
  async sendPlayerInput(input) {
    const response = await fetch('/api/game', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ input })
    });
    return response.json();
  },

  async generateImage(narrative) {
    const response = await fetch('/api/generate-image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: narrative })
    });
    return response.json();
  }
};

const StoryGameUI = () => {
  const [narrative, setNarrative] = useState('Welcome to the AI-Powered Interactive Story! Begin your adventure...');
  const [playerInput, setPlayerInput] = useState('');
  const [choices, setChoices] = useState([]);
  const [gameHistory, setGameHistory] = useState([]);
  const [currentImage, setCurrentImage] = useState('/api/placeholder/1200/800');
  const [health, setHealth] = useState(100);
  const gameContainerRef = useRef(null);

  const handlePlayerInput = async () => {
    if (!playerInput.trim()) return;

    setGameHistory(prev => [...prev, { 
      type: 'player', 
      text: playerInput 
    }]);

    try {
      const result = await GameService.sendPlayerInput(playerInput);

      setNarrative(result.narrative);
      setChoices(result.choices || []);

      const imageResponse = await GameService.generateImage(result.narrative);
      setCurrentImage(imageResponse.imageUrl || '/api/placeholder/1200/800');

      const healthChange = result.healthChange || 0;
      setHealth(prev => Math.max(0, Math.min(100, prev + healthChange)));

      setGameHistory(prev => [...prev, { 
        type: 'ai', 
        text: result.narrative 
      }]);

      setPlayerInput('');

      if (gameContainerRef.current) {
        gameContainerRef.current.scrollTop = gameContainerRef.current.scrollHeight;
      }
    } catch (error) {
      console.error('Game interaction failed:', error);
    }
  };

  return (
    <div 
      className="relative min-h-screen bg-cover bg-center flex flex-col"
      style={{ 
        backgroundImage: `url(${currentImage})`,
        backgroundBlendMode: 'overlay'
      }}
    >
      {/* Overlay to darken background image */}
      <div className="absolute inset-0 bg-black/50 pointer-events-none"></div>

      {/* Health Bar */}
      <div className="absolute top-4 right-4 z-10 flex items-center">
        <Heart className="text-red-500 mr-2" fill="currentColor" />
        <div className="w-40 bg-gray-200 rounded-full h-4 dark:bg-gray-700">
          <div 
            className="bg-red-600 h-4 rounded-full transition-all duration-300 ease-in-out" 
            style={{ 
              width: `${health}%`,
              backgroundColor: 
                health > 70 ? 'green' : 
                health > 30 ? 'orange' : 
                'red'
            }}
          ></div>
        </div>
        <span className="ml-2 text-white">{health}%</span>
      </div>

      {/* Game Content */}
      <div className="relative z-10 flex-grow flex flex-col justify-end p-8">
        {/* Narrative History */}
        <div 
          ref={gameContainerRef}
          className="flex-grow overflow-y-auto mb-4"
        >
          {gameHistory.map((entry, index) => (
            <div 
              key={index} 
              className={`mb-4 p-4 rounded-lg text-white text-opacity-90 
                ${entry.type === 'player' 
                  ? 'bg-blue-600 bg-opacity-50 text-right' 
                  : 'bg-green-600 bg-opacity-50'
                }`}
            >
              {entry.text}
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div className="flex space-x-2">
          <input 
            type="text"
            value={playerInput}
            onChange={(e) => setPlayerInput(e.target.value)}
            placeholder="Enter your action..."
            className="flex-grow p-3 bg-white bg-opacity-20 text-white rounded-lg backdrop-blur-sm"
            onKeyPress={(e) => e.key === 'Enter' && handlePlayerInput()}
          />
          <button 
            onClick={handlePlayerInput}
            className="bg-green-500 hover:bg-green-600 p-3 rounded-lg"
          >
            <Send className="text-white" />
          </button>
        </div>

        {/* Choices */}
        <div className="grid grid-cols-2 gap-2 mt-4">
          {choices.map((choice, index) => (
            <button
              key={index}
              onClick={() => {
                setPlayerInput(choice);
                handlePlayerInput();
              }}
              className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg backdrop-blur-sm bg-opacity-50 transition"
            >
              {choice}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StoryGameUI;