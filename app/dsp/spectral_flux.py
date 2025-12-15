import numpy as np
import librosa

# use 1024 and 256 if outside
def spectral_flux(pcm, sr, n_fft=512, hop=128):
    stft = np.abs(librosa.stft(pcm, n_fft=n_fft, hop_length=hop))
    flux = np.diff(stft, axis=1)
    flux = np.maximum(0, flux)
    return np.mean(flux, axis=0)


def flux_features(pcm, sr):
    flux = spectral_flux(pcm, sr)

    mean_flux = np.mean(flux)
    std_flux = np.std(flux)

    peaks = librosa.util.peak_pick(
        flux,
        pre_max=3,
        post_max=3,
        pre_avg=3,
        post_avg=3,
        delta=std_flux * 0.5, #use 0.8 for outside
        wait=10
    )

    return {
        "mean": mean_flux,
        "std": std_flux,
        "peaks": len(peaks),
    }
