import { useQuery } from '@tanstack/react-query';
import { api } from '@/api';
import type { DataStats } from '@/types/data-stats';

export function useDataStats() {
	return useQuery<DataStats>({
		queryKey: ['data-stats'],
		queryFn: async () => {
			const { data } = await api.get<DataStats>('/predict/data-stats');
			return data;
		},
	});
}
