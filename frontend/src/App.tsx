import { Header } from './components/layout/Header';
import { Footer } from './components/layout/Footer';
import { PredictionForm } from './components/prediction/PredictionForm';

function App() {
	return (
		<div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
			<Header />
			<main className="flex-1 flex items-center justify-center p-4">
				<PredictionForm />
			</main>
			<Footer />
		</div>
	);
}

export default App;
