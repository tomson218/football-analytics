import { useMutation } from '@tanstack/react-query';
import { api } from '@/api';
import type { OddsFormData } from '@/schemas/odds';
import type { PredictionResponse } from '@/types/prediction-response';

function toBackendFormat(data: OddsFormData) {
	return {
		odd_home: data.oddHome,
		odd_away: data.oddAway,
		max_home: data.maxHome,
		max_draw: data.maxDraw,
		max_away: data.maxAway,
		handi_size: data.handiSize,
	};
}

export async function predictHomeNoLose(data: OddsFormData): Promise<PredictionResponse> {
	const response = await api.post<PredictionResponse>('/predict/home-no-lose', toBackendFormat(data));
	return response.data;
}

export function usePredictHomeNoLose() {
	return useMutation<PredictionResponse, Error, OddsFormData>({
		mutationFn: predictHomeNoLose,
	});
}
