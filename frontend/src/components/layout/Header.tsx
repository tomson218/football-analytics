import { BarChart3, Globe } from 'lucide-react';

export function Header() {
	return (
		<header className="sticky top-0 z-50 w-full border-b border-white/20 bg-white/80 backdrop-blur-md shadow-sm">
			<nav className="max-w-6xl mx-auto flex items-center justify-between px-6 py-3" aria-label="Main navigation">
				{/* Logo and title */}
				<div className="flex items-center gap-2">
					<BarChart3 className="text-indigo-600" size={24} />
					<h1 className="text-lg font-bold tracking-tight text-slate-800">
						Football Analytics
					</h1>
					<span className="ml-2 text-[10px] font-semibold uppercase tracking-wider text-indigo-500 bg-indigo-50 px-2 py-0.5 rounded-full">
						Prediction
					</span>
				</div>

				{/* Navigation links */}
				<div className="flex items-center gap-4">
					<a
						href="https://github.com"
						target="_blank"
						rel="noopener noreferrer"
						className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 transition-colors"
					>
 					<Globe size={16} />
						<span className="hidden sm:inline">GitHub</span>
					</a>
				</div>
			</nav>
		</header>
	);
}
