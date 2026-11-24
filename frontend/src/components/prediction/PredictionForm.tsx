import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { TrendingUp, Home, Shuffle, Plane, Target, BarChart3, MinusCircle } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Label } from '@/components/ui/Label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Spinner } from '@/components/ui/Spinner';
import { oddsLimits, oddsSchema, type OddsFormData } from '@/schemas/odds';
import { usePredictHomeNoLose } from '@/api/mutations/use-predict-home-no-lose';
import { useFeatureImportance } from '@/api/queries/use-feature-importance';
import { ResultDisplay } from './ResultDisplay';
import type { FeatureImportance } from '@/types/feature-importance';

// Labels, icons, input hints and feature importance keys for each form field
const fieldConfig: Record<
	keyof OddsFormData,
	{ label: string; icon: React.ReactNode; step: string; placeholder: string; importanceKey: keyof FeatureImportance }
> = {
	oddHome: { label: 'Odd Home', icon: <Home size={14} />, step: '0.01', placeholder: '1.85', importanceKey: 'odd_home' },
	oddAway: { label: 'Odd Away', icon: <Plane size={14} />, step: '0.01', placeholder: '4.20', importanceKey: 'odd_away' },
	maxHome: { label: 'Max Home', icon: <TrendingUp size={14} />, step: '0.01', placeholder: '1.90', importanceKey: 'max_home' },
	maxDraw: { label: 'Max Draw', icon: <Shuffle size={14} />, step: '0.01', placeholder: '3.50', importanceKey: 'max_draw' },
	maxAway: { label: 'Max Away', icon: <TrendingUp size={14} />, step: '0.01', placeholder: '4.30', importanceKey: 'max_away' },
	handiSize: { label: 'Handi Size', icon: <MinusCircle size={14} />, step: '0.1', placeholder: '-0.3', importanceKey: 'handi_size' },
};

export function PredictionForm() {
	const {
		register,
		handleSubmit,
		formState: { errors },
		reset,
	} = useForm({
		resolver: zodResolver(oddsSchema),
		defaultValues: {
			oddHome: oddsLimits.oddHome.min,
			oddAway: oddsLimits.oddAway.min,
			maxHome: oddsLimits.maxHome.min,
			maxDraw: oddsLimits.maxDraw.min,
			maxAway: oddsLimits.maxAway.min,
			handiSize: oddsLimits.handiSize.min,
		},
	});

	const mutation = usePredictHomeNoLose();
	const { isPending, error: err, isError, isSuccess: success, data: predictionData } = mutation;
	const errorMessage = err?.message ?? '';

	const { data: importance } = useFeatureImportance();

	const onSubmit = (data: OddsFormData) => {
		mutation.mutate(data);
	};

	const renderField = (name: keyof OddsFormData) => {
		const { message } = errors[name] ?? {};
		const { label, icon, step, placeholder, importanceKey } = fieldConfig[name];
		const { min, max } = oddsLimits[name];
		const importancePercent = importance?.[importanceKey];
		return (
			<div className='space-y-1.5'>
				<Label htmlFor={name} className='flex items-center gap-1.5 text-xs font-medium text-slate-600'>
					{icon}
					{label}
					{importancePercent != null ? (
						<span className='text-[10px] font-medium text-indigo-500 bg-indigo-50 px-1.5 py-0.5 rounded'>
							{importancePercent}%
						</span>
					) : null}
				</Label>
				<Input
					id={name}
					type='number'
					min={min}
					max={max}
					step={step}
					placeholder={placeholder}
					className='h-10'
					{...register(name, { valueAsNumber: true })}
				/>
				{message && <p className='text-xs text-red-500'>{message as string}</p>}
			</div>
		);
	};

	const renderColumn = (fields: (keyof OddsFormData)[], groupLabel: string, icon: React.ReactNode) => (
		<div className='space-y-3'>
			<div className='flex items-center gap-2 pb-2 border-b border-slate-200'>
				<span className='text-slate-500'>{icon}</span>
				<p className='text-xs font-semibold uppercase tracking-wider text-slate-500'>{groupLabel}</p>
			</div>
			<div className='space-y-3'>
				{fields.map(name => (
					<div key={name}>{renderField(name)}</div>
				))}
			</div>
		</div>
	);

	return (
		<Card className='w-full max-w-lg mx-auto shadow-xl border-0 bg-white/80 backdrop-blur-sm'>
			{/* Header with gradient */}
			<CardHeader className='pb-4'>
				<div className='rounded-xl bg-gradient-to-r from-indigo-600 to-blue-600 p-5 -mx-5 -mt-5 mb-5 shadow-md'>
					<div className='flex items-center gap-3'>
						<div className='flex h-10 w-10 items-center justify-center rounded-lg bg-white/20 backdrop-blur-sm'>
							<Target className='text-white' size={20} />
						</div>
						<div>
							<CardTitle className='text-white text-lg'>Home No Lose Predictor</CardTitle>
							<CardDescription className='text-indigo-100 text-xs mt-0.5'>
								CatBoost 6-feature model — top 6 features by importance, AUC 0.72
							</CardDescription>
						</div>
					</div>
				</div>
			</CardHeader>
			<CardContent className='pt-0'>
				<form onSubmit={handleSubmit(onSubmit)} className='space-y-5'>
					{/* Two columns: Average Odds | Max Odds, plus HandiSize row */}
					<div className='grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-md mx-auto sm:max-w-none'>
						{renderColumn(['oddHome', 'oddAway'], 'Average Odds', <BarChart3 size={12} />)}
						{renderColumn(['maxHome', 'maxDraw', 'maxAway'], 'Max Odds', <TrendingUp size={12} />)}
					</div>

					{/* HandiSize — single field row */}
					<div className='max-w-md mx-auto sm:max-w-none'>{renderField('handiSize')}</div>

					{/* Submit button (centered on mobile) */}
					<div className='max-w-md mx-auto sm:max-w-none'>
						<Button
							type='submit'
							className='w-full h-11 text-base font-semibold bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 shadow-lg shadow-indigo-200 transition-all duration-200'
							disabled={isPending}>
							{isPending ? (
								<>
									<Spinner size={16} />
									Predicting...
								</>
							) : (
								<>
									<Target size={16} />
									Predict
								</>
							)}
						</Button>
					</div>
				</form>

				{/* Error message */}
				{isError && (
					<div className='mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600 flex items-center gap-2'>
						<Plane size={14} />
						{errorMessage}
					</div>
				)}

				{/* Results */}
				{success && predictionData && <ResultDisplay data={predictionData} />}

				{/* Reset button */}
				{success && (
					<Button
						variant='outline'
						className='mt-4 w-full h-10'
						onClick={() => {
							mutation.reset();
							reset();
						}}>
						New Prediction
					</Button>
				)}
			</CardContent>
		</Card>
	);
}
