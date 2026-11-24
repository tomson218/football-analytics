import { useQuery } from '@tanstack/react-query';
import { api } from '@/api';
import type { FeatureImportance } from '@/types/feature-importance';

export async function fetchFeatureImportance(): Promise<FeatureImportance> {
	const response = await api.get<FeatureImportance>('/predict/feature-importance');
	return response.data;
}

export function useFeatureImportance() {
	return useQuery<FeatureImportance, Error>({
		queryKey: ['feature-importance'],
		queryFn: fetchFeatureImportance,
	});
}
