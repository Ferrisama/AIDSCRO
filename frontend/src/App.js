import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Container,
  Typography,
  TextField,
  Button,
  Grid,
  Paper,
} from "@material-ui/core";
import { Alert } from "@material-ui/lab";

function App() {
  const [prediction, setPrediction] = useState(null);
  const [featureImportance, setFeatureImportance] = useState(null);
  const [error, setError] = useState(null);

  const [inputData, setInputData] = useState({
    start_location: "",
    end_location: "",
    distance: 0,
    traffic_density: 0,
    weather_condition: "",
    temperature: 0,
    is_holiday: 0,
    hour: 0,
    day_of_week: 0,
    month: 0,
    is_weekend: 0,
  });

  useEffect(() => {
    fetchFeatureImportance();
  }, []);

  const fetchFeatureImportance = async () => {
    try {
      const response = await axios.get(
        "http://localhost:8000/feature_importance"
      );
      setFeatureImportance(response.data);
    } catch (error) {
      setError("Failed to fetch feature importance");
    }
  };

  const handleInputChange = (event) => {
    setInputData({
      ...inputData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/predict",
        inputData
      );
      setPrediction(response.data.predicted_travel_time);
      setError(null);
    } catch (error) {
      setError("Failed to make prediction");
      setPrediction(null);
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h2" align="center" gutterBottom>
        AIDSCRO Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper style={{ padding: 16 }}>
            <Typography variant="h5" gutterBottom>
              Make a Prediction
            </Typography>
            <form onSubmit={handleSubmit}>
              {Object.keys(inputData).map((key) => (
                <TextField
                  key={key}
                  fullWidth
                  label={key.replace("_", " ")}
                  name={key}
                  value={inputData[key]}
                  onChange={handleInputChange}
                  margin="normal"
                />
              ))}
              <Button type="submit" variant="contained" color="primary">
                Predict
              </Button>
            </form>
            {prediction && (
              <Typography variant="h6" style={{ marginTop: 16 }}>
                Predicted Travel Time: {prediction.toFixed(2)} hours
              </Typography>
            )}
            {error && <Alert severity="error">{error}</Alert>}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper style={{ padding: 16 }}>
            <Typography variant="h5" gutterBottom>
              Feature Importance
            </Typography>
            {featureImportance && (
              <ul>
                {Object.entries(featureImportance).map(
                  ([feature, importance]) => (
                    <li key={feature}>
                      {feature}: {importance.toFixed(4)}
                    </li>
                  )
                )}
              </ul>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;
