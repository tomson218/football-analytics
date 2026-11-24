// Feature importance for 6-feature production model (top 6 by importance)
// Backend returns all 6 features used in the model:
// 5 odds (OddHome, OddAway, MaxHome, MaxDraw, MaxAway) and the Asian Handicap (HandiSize)
export interface FeatureImportance {
	odd_home: number;
	odd_away: number;
	max_home: number;
	max_draw: number;
	max_away: number;
	handi_size: number;
}
