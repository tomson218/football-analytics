import { useQuery } from '@tanstack/react-query';
import { api } from '@/api';
import type { ModelMetrics } from '@/types/model-metrics';

export async function fetchModelMetrics(): Promise<ModelMetrics> {
	const response = await api.get<ModelMetrics>('/predict/model-metrics');
	return response.data;
}

export function useModelMetrics() {
	return useQuery<ModelMetrics, Error>({
		queryKey: ['model-metrics'],
		queryFn: fetchModelMetrics,
	});
}
