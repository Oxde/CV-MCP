import { ChevronLeft } from 'lucide-react';

export default function OnboardingStep({
  step,
  totalSteps,
  title,
  subtitle,
  onBack,
  onNext,
  onSkip,
  canContinue = true,
  children,
}) {
  const progress = ((step + 1) / totalSteps) * 100;

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col">
      {/* Progress bar */}
      <div className="w-full h-1 bg-gray-800">
        <div
          className="h-full bg-white transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Top bar */}
      <div className="flex items-center justify-between px-4 py-3">
        {step > 0 ? (
          <button
            onClick={onBack}
            className="flex items-center gap-1 text-sm text-gray-400 hover:text-white transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
            Back
          </button>
        ) : (
          <div />
        )}
        <span className="text-xs text-gray-500">
          {step + 1} / {totalSteps}
        </span>
        {onSkip ? (
          <button
            onClick={onSkip}
            className="text-sm text-gray-500 hover:text-gray-300 transition-colors"
          >
            Skip
          </button>
        ) : (
          <div />
        )}
      </div>

      {/* Content */}
      <div className="flex-1 flex flex-col items-center justify-center px-4 py-8 max-w-lg mx-auto w-full animate-slide-right">
        {title && (
          <h1 className="text-2xl md:text-3xl font-bold text-white text-center mb-2">
            {title}
          </h1>
        )}
        {subtitle && (
          <p className="text-gray-400 text-center mb-8">{subtitle}</p>
        )}
        <div className="w-full">{children}</div>
      </div>

      {/* Bottom */}
      <div className="px-4 pb-8 max-w-lg mx-auto w-full">
        <button
          onClick={onNext}
          disabled={!canContinue}
          className="w-full bg-white hover:bg-gray-100 disabled:bg-gray-700 disabled:text-gray-500 text-gray-950 font-semibold py-3.5 rounded-xl text-lg transition-all active:scale-[0.98]"
        >
          Continue
        </button>
      </div>
    </div>
  );
}
