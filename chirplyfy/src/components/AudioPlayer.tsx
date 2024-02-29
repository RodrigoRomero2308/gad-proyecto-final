import { useEffect, useRef, useState } from "react";
import WaveSurfer from "wavesurfer.js";
import Spectrogram from "wavesurfer.js/dist/plugins/spectrogram";
import {
  IonActionSheet,
  IonButton,
  IonButtons,
  IonContent,
  IonHeader,
  IonIcon,
  IonModal,
  IonTitle,
  IonToolbar,
} from "@ionic/react";
import {
  ellipsisVertical,
  pause,
  play,
  playBack,
  playOutline,
} from "ionicons/icons";
import colormap from "colormap";

const AudioPlayer = ({
  url,
  id,
  mode,
}: {
  url: string;
  id: string;
  mode?: "with-spectrogram" | "normal";
}) => {
  if (!mode) mode = "normal";
  const waveRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLDivElement>(null);
  const [playing, setPlaying] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const wavesurferInstance = useRef<WaveSurfer>();

  useEffect(() => {
    if (!waveRef.current) return;
    const rootStyle = getComputedStyle(document.documentElement);
    const primaryColor = rootStyle.getPropertyValue("--ion-color-primary");
    const secondaryColor = rootStyle.getPropertyValue("--ion-color-secondary");

    const waveSurfer = WaveSurfer.create({
      container: waveRef.current,
      waveColor: primaryColor,
      progressColor: secondaryColor,
      height: 48,
      barWidth: 2,
      barGap: 1,
      barRadius: 2,
    });

    wavesurferInstance.current = waveSurfer;

    waveSurfer.load(url);

    if (canvasRef.current)
      waveSurfer.registerPlugin(
        Spectrogram.create({
          labels: true,
          container: canvasRef.current || undefined,
          fftSamples: 1024,
          colorMap: colormap({
            colormap: "chlorophyll",
            nshades: 256,
            format: "float",
          }),
        })
      );

    waveSurfer.on("finish", () => {
      setPlaying(false);
    });

    return () => {
      waveSurfer.destroy();
    };
  }, [url]);

  const handlePlay = () => {
    setPlaying((value) => !value);
    wavesurferInstance.current?.playPause();
  };

  const handleReset = () => {
    wavesurferInstance.current?.setTime(0);
  };

  return (
    <div>
      <div
        style={{
          display: "flex",
        }}
      >
        <IonButton size="small" fill="clear" onClick={handlePlay}>
          <IonIcon icon={playing ? pause : play} />
        </IonButton>
        <IonButton size="small" fill="clear" onClick={handleReset}>
          <IonIcon icon={playBack} />
        </IonButton>
        <div
          style={{
            flex: 1,
          }}
          ref={waveRef}
        ></div>
        {mode === "normal" ? (
          <>
            <IonButton id={`action-sheet-${id}`} size="small" fill="clear">
              <IonIcon icon={ellipsisVertical} />
            </IonButton>
            <IonActionSheet
              trigger={`action-sheet-${id}`}
              header="Actions"
              buttons={[
                {
                  text: "See spectrogram",
                  role: "spectrogram",
                },
                {
                  text: "Cancel",
                  role: "cancel",
                },
              ]}
              onDidDismiss={({ detail }) => {
                if (detail.role === "spectrogram") setIsModalOpen(true);
              }}
            ></IonActionSheet>
            <IonModal isOpen={isModalOpen}>
              <IonHeader>
                <IonToolbar>
                  <IonTitle>Audio details</IonTitle>
                  <IonButtons slot="end">
                    <IonButton onClick={() => setIsModalOpen(false)}>
                      Close
                    </IonButton>
                  </IonButtons>
                </IonToolbar>
              </IonHeader>
              <IonContent className="ion-padding">
                <AudioPlayer
                  url={url}
                  id={id + "-preview"}
                  mode="with-spectrogram"
                />
              </IonContent>
            </IonModal>
          </>
        ) : null}
      </div>
      {mode === "with-spectrogram" ? <div ref={canvasRef}></div> : null}
    </div>
  );
};

export default AudioPlayer;
