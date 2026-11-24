export interface PredictionResponse {
	probability: number; // P(HomeNoLose) from CatBoost model
	implied_probability: number; // Implied probability from odds
	is_value_bet: boolean | null; // Value bet flag
}
