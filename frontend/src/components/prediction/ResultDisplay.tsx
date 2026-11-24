import { Target, BarChart3 } from 'lucide-react';
import type { PredictionResponse } from '@/types/prediction-response';

interface ResultDisplayProps {
	data: PredictionResponse;
}

export function ResultDisplay({ data: { probability, implied_probability, is_value_bet } }: ResultDisplayProps) {
	const probPercent = (probability * 100).toFixed(1);
	const impliedPercent = (implied_probability * 100).toFixed(1);
	const probNumber = probability * 100;

	return (
		<section className="mt-6 space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500" aria-label="Prediction result">
			{/* Main probability card */}
			<article className="rounded-xl border-2 border-indigo-200 bg-gradient-to-br from-indigo-50 via-white to-blue-50 p-6 text-center shadow-lg">
				<figcaption className="flex items-center justify-center gap-2 mb-3">
					<Target className="text-indigo-600" size={20} />
					<p className="text-sm font-medium text-indigo-700">
						P(Home No Lose)
					</p>
				</figcaption>
				<p className="text-5xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-600 to-blue-600 bg-clip-text text-transparent">
					{probPercent}%
				</p>
				{/* Progress bar */}
				<figure className="mt-4 h-3 w-full rounded-full bg-indigo-100 overflow-hidden" aria-label={`Probability: ${probPercent}%`}>
					<div
						className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-blue-500 transition-all duration-700 ease-out"
						style={{ width: `${probNumber}%` }}
					/>
				</figure>
			</article>

			{/* Detail cards */}
			<dl className="grid grid-cols-2 gap-3">
				<div className="rounded-xl border bg-white p-4 text-center shadow-sm">
					<dt className="flex items-center justify-center gap-1.5 mb-1">
						<BarChart3 size={14} className="text-muted-foreground" />
						<p className="text-xs font-medium text-muted-foreground">Implied Probability</p>
					</dt>
					<dd className="text-xl font-bold text-slate-800">{impliedPercent}%</dd>
				</div>
				<div className="rounded-xl border bg-white p-4 text-center shadow-sm">
					<dt className="flex items-center justify-center gap-1.5 mb-1">
						<p className="text-xs font-medium text-muted-foreground">Value Bet</p>
					</dt>
					<dd className={`text-xl font-bold ${is_value_bet === true ? 'text-emerald-600' : is_value_bet === false ? 'text-red-500' : 'text-muted-foreground'}`}>
						{is_value_bet === true ? '✓ Yes' : is_value_bet === false ? '✗ No' : '—'}
					</dd>
				</div>
			</dl>
		</section>
	);
}
