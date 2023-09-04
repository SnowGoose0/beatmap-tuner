import axios from 'axios';
import { useState, useEffect } from 'react';
import './Modifier.scss'

const roundFloat = (value, digits) => {
  if (value == undefined) return;
  if (value.toFixed == undefined) return;

  return value.toFixed(digits);
}

const Modifier = (props) => {
  const { settings, id } = props;
  const [AR, setAR] = useState(0)
  const [HP, setHP] = useState(0)
  const [CS, setCS] = useState(0)
  const [OD, setOD] = useState(0)
  const [rate, setRate] = useState(0)
  const [BPM, setBPM] = useState(0)

  const handleHPChange = (e) => setHP(e.target.value);
  const handleCSChange = (e) => setCS(e.target.value);
  const handleARChange = (e) => setAR(e.target.value);
  const handleODChange = (e) => setOD(e.target.value);
  const handleBPMChange = (e) => setBPM(e.target.value);

  const handleSetDefault = () => {
    setAR(settings.ar);
    setHP(settings.hp);
    setCS(settings.cs);
    setOD(settings.od);
    setRate(settings.rate);
    setBPM(roundFloat(settings.bpm));
  }

  const handleOszExport = async (e) => {
    e.preventDefault();

    const exportSettings = {
      'hp': HP,
      'ar': AR,
      'cs': CS,
      'od': OD,
      'bpm': BPM,
      'rate': rate, 
    }

    const response = await axios
      .post('http://localhost:5000/difficulty-export', 
      {
        'fid': id,
        'fdata': exportSettings,
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

  }

  useEffect(() => {
    handleSetDefault();
  }, [settings]);
  
  return (
    <div className="modifier">
      <div className="modifier-container">
        <label htmlFor="hp" className="hp-label">HP: {HP}</label>
        <input 
          type="range" 
          className="hp-modifier mod-range"
          step="0.1"
          id="hp" 
          min="0" 
          max="10" 
          value={HP} 
          onChange={handleHPChange}
        />

        <label htmlFor="cs" className="cs-label">CS: {CS}</label>
        <input 
          type="range" 
          className="cs-modifier mod-range"
          step="0.1" 
          id="cs" 
          min="0" 
          max="10" 
          value={CS}
          onChange={handleCSChange}
        />

        <label htmlFor="ar" className="ar-label">AR: {AR}</label>
        <input 
          type="range" 
          className="ar-modifier mod-range"
          step="0.1"  
          id="ar" 
          min="0" 
          max="10" 
          value={AR}
          onChange={handleARChange}
        />

        <label htmlFor="od" className="od-label">OD: {OD}</label>
        <input 
          type="range" 
          className="od-modifier mod-range"
          step="0.1"  
          id="od" 
          min="0" 
          max="10" 
          value={OD}
          onChange={handleODChange}
        />

        <label htmlFor="bpm" className="bpm-label">BPM: {BPM}</label>
        <input 
          type="number" 
          className="bpm-modifier mod-input" 
          id="bpm" 
          value={BPM}
          onChange={handleBPMChange}
        />
      </div>
      <div className="modifier-buttons">
        <button className="modify-reset btn" onClick={handleSetDefault}>Reset</button>
        <button className="modify-export btn" onClick={handleOszExport}>Export</button>
      </div>
    </div>
  )
}

export default Modifier;