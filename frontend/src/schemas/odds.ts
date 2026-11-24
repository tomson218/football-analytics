import { z } from 'zod';

// Allowed input ranges (matching backend validation)
export const oddsLimits = {
	oddHome: { min: 1.04, max: 26.13 },
	oddAway: { min: 1.08, max: 41.22 },
	maxHome: { min: 1.06, max: 35 },
	maxDraw: { min: 2.2, max: 24 },
	maxAway: { min: 1.1, max: 65 },
	handiSize: { min: -3.5, max: 2.8 },
};

const limitedNumber = (name: string, { min, max }: { min: number; max: number }) =>
	z.number().min(min, `${name} must be at least ${min}`).max(max, `${name} cannot exceed ${max}`);

export const oddsSchema = z.object({
	oddHome: limitedNumber('Odd Home', oddsLimits.oddHome),
	oddAway: limitedNumber('Odd Away', oddsLimits.oddAway),
	maxHome: limitedNumber('Max Home', oddsLimits.maxHome),
	maxDraw: limitedNumber('Max Draw', oddsLimits.maxDraw),
	maxAway: limitedNumber('Max Away', oddsLimits.maxAway),
	handiSize: limitedNumber('Handicap', oddsLimits.handiSize),
});

export type OddsFormData = z.infer<typeof oddsSchema>;
