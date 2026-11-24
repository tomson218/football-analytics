import { BarChart3, Database, Brain, GitBranch } from 'lucide-react';
import { getCurrentYear } from '@/lib/utils';
import { useModelMetrics } from '@/api/queries/use-model-metrics';
import { useDataStats } from '@/api/queries/use-data-stats';

export function Footer() {
	const { data: metrics } = useModelMetrics();
	const { data: stats } = useDataStats();

	return (
		<footer className="w-full border-t border-slate-200 bg-white/80 backdrop-blur-sm mt-auto" role="contentinfo">
			<div className="max-w-6xl mx-auto px-6 py-6">
				{/* Top section: columns */}
				<div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-6">
					{/* About */}
					<section>
						<h2 className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-2">
							<BarChart3 size={14} className="text-indigo-500" />
							Football Analytics
						</h2>
						<p className="text-xs text-slate-500 leading-relaxed">
							Predict home team no-lose probability using CatBoost ML model trained on football match data from top European leagues.
						</p>
					</section>

					{/* Tech Stack */}
					<section>
						<h2 className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-2">
							<GitBranch size={14} className="text-indigo-500" />
							Tech Stack
						</h2>
						<ul className="text-xs text-slate-500 space-y-1">
							<li>React 19 + TypeScript + Vite</li>
							<li>FastAPI + CatBoost + MySQL</li>
							<li>Data Warehouse (Star Schema)</li>
						</ul>
					</section>

					{/* Data */}
					<section>
						<h2 className="flex items-center gap-2 text-sm font-semibold text-slate-700 mb-2">
							<Database size={14} className="text-indigo-500" />
							Data
						</h2>
						<ul className="text-xs text-slate-500 space-y-1">
							<li>
								{stats ? `${stats.total_matches.toLocaleString()} matches • ${stats.total_leagues} leagues` : '—'}
							</li>
							<li>
								{stats ? `Seasons ${stats.season_start} – ${stats.season_end}` : '—'}
							</li>
							<li>
								<a
									href="https://www.kaggle.com/datasets/adamgbor/club-football-match-data-2000-2025"
									target="_blank"
									rel="noopener noreferrer"
									className="text-indigo-500 hover:text-indigo-700 underline"
								>
									Kaggle Dataset
								</a>
							</li>
						</ul>
					</section>
				</div>

				{/* Bottom bar */}
				<div className="border-t border-slate-100 pt-4 flex flex-col sm:flex-row items-center justify-between gap-2">
					<p className="text-xs text-slate-400">
						© {getCurrentYear()} Football Analytics. Built with React, FastAPI & CatBoost.
					</p>
					<div className="flex items-center gap-3 text-xs text-slate-400">
						<span className="flex items-center gap-1">
							<Brain size={12} />
							Model AUC: {metrics?.test_auc ?? '—'}
						</span>
					</div>
				</div>
			</div>
		</footer>
	);
}
