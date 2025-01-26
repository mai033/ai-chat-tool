import React, { useState, useEffect } from 'react';
import {
  TextField,
  Button,
  CircularProgress,
  MenuItem,
  Select,
  Container,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';

interface ModelOption {
  value: string;
  label: string;
}

// Allowed models to be displayed in the dropdown
const allowedModels = new Set([
  'gpt-4o',
  'gpt-4o-mini',
  'gpt-4',
  'gpt-3.5-turbo',
  'claude-3-5-sonnet-20241022',
  'claude-3-5-haiku-20241022',
]);

const App: React.FC = () => {
  const [models, setModels] = useState<ModelOption[]>([]);
  const [model, setModel] = useState<string>('');
  const [systemPrompt, setSystemPrompt] = useState<string>('');
  const [userInput, setUserInput] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [chatHistory, setChatHistory] = useState<
    { input: string; output: string }[]
  >([]);

  // Fetch available models from the backend and filter only the allowed ones
  useEffect(() => {
    const fetchModels = async () => {
      try {
        const res = await fetch('http://127.0.0.1:5000/models');
        const data = await res.json();

        if (data.models) {
          // Filter the models to include only those in the allowedModels set
          const filteredModels = data.models
            .filter((m: { id: string }) => allowedModels.has(m.id))
            .map((m: { id: string; provider: string }) => ({
              value: m.id,
              label: `${m.provider.toUpperCase()} - ${m.id}`,
            }));

          setModels(filteredModels);
        }
      } catch (error) {
        console.error('Error fetching models:', error);

        // Use fallback model list if the backend request fails
        setModels([
          { value: 'gpt-4o', label: 'OpenAI - gpt-4o' },
          { value: 'gpt-4o-mini', label: 'OpenAI - gpt-4o-mini' },
          { value: 'gpt-4', label: 'OpenAI - gpt-4' },
          { value: 'gpt-3.5-turbo', label: 'OpenAI - gpt-3.5-turbo' },
          {
            value: 'claude-3-5-sonnet-20241022',
            label: 'Anthropic - claude-3-5-sonnet-20241022',
          },
          {
            value: 'claude-3-5-haiku-20241022',
            label: 'Anthropic - claude-3-5-haiku-20241022',
          },
        ]);
      }
    };

    fetchModels();
  }, []);

  // Handle form submission and send chat request to the backend
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!model) {
      alert('Please select a model.');
      return;
    }

    setLoading(true); // Show loading indicator
    setResponse(''); // Clear previous response

    try {
      const res = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model,
          system_prompt: systemPrompt,
          user_input: userInput,
        }),
      });

      const data = await res.json();
      const newResponse = data.response || 'Error: ' + data.error;
      setResponse(newResponse);

      // Update chat history
      setChatHistory((prev) => [
        ...prev,
        { input: userInput, output: newResponse },
      ]);
    } catch (error) {
      setResponse('Error: ' + (error as Error).message);
    } finally {
      setLoading(false); // Hide loading indicator after request completes
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#e0e0e0',
        width: '100vw',
        padding: 2,
      }}
    >
      <Container
        maxWidth="sm"
        sx={{
          backgroundColor: 'white',
          padding: 4,
          borderRadius: 2,
          boxShadow: 3,
          textAlign: 'center',
        }}
      >
        {/* App Title */}
        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{ color: 'black' }}
        >
          AI Chat Tool
        </Typography>

        {/* Chat Form */}
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
        >
          {/* Model selection dropdown */}
          <Select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            displayEmpty
            fullWidth
          >
            <MenuItem value="" disabled>
              Select Model
            </MenuItem>
            {models.map((m) => (
              <MenuItem key={m.value} value={m.value}>
                {m.label}
              </MenuItem>
            ))}
          </Select>

          {/* System prompt input field */}
          <TextField
            label="System Prompt (Optional)"
            variant="outlined"
            multiline
            fullWidth
            value={systemPrompt}
            onChange={(e) => setSystemPrompt(e.target.value)}
          />

          {/* User input text area */}
          <TextField
            label="User Input"
            variant="outlined"
            multiline
            required
            fullWidth
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
          />

          {/* Submit button with loading spinner */}
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Submit'}
          </Button>
        </Box>

        {/* Response Box */}
        {response && (
          <Box
            mt={4}
            p={2}
            sx={{
              backgroundColor: '#ffffff',
              borderRadius: 1,
              color: 'black',
              textAlign: 'center',
              boxShadow: 1,
            }}
          >
            <Typography variant="h6">Response:</Typography>
            <Typography>{response}</Typography>
          </Box>
        )}

        {/* Chat History Section */}
        {chatHistory.length > 0 && (
          <Box mt={4}>
            <Typography
              variant="h5"
              sx={{ fontWeight: 'bold', marginBottom: 2, color: 'black' }}
            >
              History
            </Typography>
            <List
              sx={{
                backgroundColor: '#f5f5f5',
                borderRadius: 1,
                color: 'black',
                maxHeight: 300,
                overflowY: 'auto',
                padding: 2,
                boxShadow: 1,
              }}
            >
              {chatHistory.map((entry, index) => (
                <ListItem
                  key={index}
                  sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'flex-start',
                  }}
                >
                  <ListItemText
                    primary={`User: ${entry.input}`}
                    sx={{ fontWeight: 'bold', color: 'black' }}
                  />
                  <ListItemText
                    primary={`Bot: ${entry.output}`}
                    sx={{ color: 'black' }}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        )}
      </Container>
    </Box>
  );
};

export default App;
