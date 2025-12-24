"""
Visualization Router for F1 Race Strategy Simulator API

This router provides visualization endpoints for telemetry data analysis.
Supports both interactive Plotly JSON charts and static PNG images.

Endpoints:
- /speed-trace: Speed comparison between two drivers
- /throttle-brake: Speed, throttle, and brake analysis
- /lap-time-distribution: Lap time box plots
- /sector-comparison: Sector performance bar chart
- /tyre-degradation: Lap time vs tyre age
- /gear-usage: Gear changes visualization
- /performance-radar: Multi-metric radar chart
- /health: Check visualization library availability
"""

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from typing import Literal, Optional
import io
import logging

# Import FastF1 client for data retrieval
from shared.clients.fastf1_client import FastF1Client

logger = logging.getLogger(__name__)

# Check for visualization libraries
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger.warning("Plotly not installed. JSON visualizations will be unavailable.")

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.warning("Matplotlib not installed. PNG visualizations will be unavailable.")

router = APIRouter(prefix="/api/v1/visualizations")

# F1 Team Colors
TEAM_COLORS = {
    "default_primary": "#0600EF",  # Blue
    "default_secondary": "#FF1801",  # Red
    "background": "#FFFFFF",
    "grid": "#E5E5E5"
}


@router.get("/speed-trace")
async def get_speed_trace(
    year: int = Query(..., description="Season year"),
    event: str = Query(..., description="Event name (e.g., 'Monaco', 'Silverstone')"),
    session: str = Query(..., description="Session type (FP1, FP2, FP3, Q, R)"),
    driver1: str = Query(..., description="First driver code (e.g., 'VER')"),
    driver2: str = Query(..., description="Second driver code (e.g., 'LEC')"),
    format: Literal["json", "png"] = Query("json", description="Output format")
):
    """
    Compare speed traces between two drivers on their fastest laps.
    
    Returns:
    - format=json: Plotly JSON for interactive charts
    - format=png: PNG image file
    """
    try:
        client = FastF1Client()
        
        # Get session data
        session_data = client.get_session(year, event, session)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get fastest laps for both drivers
        laps1 = client.get_driver_laps(year, event, session, driver1)
        laps2 = client.get_driver_laps(year, event, session, driver2)
        
        if laps1.empty or laps2.empty:
            raise HTTPException(status_code=404, detail="Lap data not found for one or both drivers")
        
        # Get fastest lap for each driver using pick_fastest()
        fastest_lap1 = laps1.pick_fastest()
        fastest_lap2 = laps2.pick_fastest()
        
        # Get telemetry data
        telemetry1 = fastest_lap1.get_telemetry()
        telemetry2 = fastest_lap2.get_telemetry()
        
        if telemetry1.empty or telemetry2.empty:
            raise HTTPException(status_code=404, detail="Telemetry data not available")
        
        if format == "json":
            if not PLOTLY_AVAILABLE:
                raise HTTPException(status_code=503, detail="Plotly not installed")
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=telemetry1['Distance'],
                y=telemetry1['Speed'],
                mode='lines',
                name=f'{driver1} ({fastest_lap1["LapTime"]})',
                line=dict(color=TEAM_COLORS["default_primary"], width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=telemetry2['Distance'],
                y=telemetry2['Speed'],
                mode='lines',
                name=f'{driver2} ({fastest_lap2["LapTime"]})',
                line=dict(color=TEAM_COLORS["default_secondary"], width=2)
            ))
            
            fig.update_layout(
                title=f'Speed Comparison: {driver1} vs {driver2}<br>{year} {event} - {session}',
                xaxis_title='Distance (m)',
                yaxis_title='Speed (km/h)',
                hovermode='x unified',
                template='plotly_white',
                height=500
            )
            
            return {
                "plotly_json": fig.to_json(),
                "type": "plotly"
            }
        
        else:  # PNG format
            if not MATPLOTLIB_AVAILABLE:
                raise HTTPException(status_code=503, detail="Matplotlib not installed")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ax.plot(telemetry1['Distance'], telemetry1['Speed'], 
                   color=TEAM_COLORS["default_primary"], linewidth=2, 
                   label=f'{driver1} ({fastest_lap1["LapTime"]})')
            ax.plot(telemetry2['Distance'], telemetry2['Speed'], 
                   color=TEAM_COLORS["default_secondary"], linewidth=2, 
                   label=f'{driver2} ({fastest_lap2["LapTime"]})')
            
            ax.set_xlabel('Distance (m)', fontsize=12)
            ax.set_ylabel('Speed (km/h)', fontsize=12)
            ax.set_title(f'Speed Comparison: {driver1} vs {driver2}\n{year} {event} - {session}', 
                        fontsize=14, fontweight='bold')
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
            # Save to bytes buffer
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error generating speed trace: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/throttle-brake")
async def get_throttle_brake_analysis(
    year: int = Query(..., description="Season year"),
    event: str = Query(..., description="Event name"),
    session: str = Query(..., description="Session type"),
    driver1: str = Query(..., description="First driver code"),
    driver2: str = Query(..., description="Second driver code"),
    format: Literal["json", "png"] = Query("json", description="Output format")
):
    """
    Analyze speed, throttle, and brake application for two drivers.
    
    Returns 3-panel visualization showing:
    - Speed trace
    - Throttle application (0-100%)
    - Brake application (0-100%)
    """
    try:
        client = FastF1Client()
        
        # Get session and lap data
        session_data = client.get_session(year, event, session)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        laps1 = client.get_driver_laps(year, event, session, driver1)
        laps2 = client.get_driver_laps(year, event, session, driver2)
        
        if laps1.empty or laps2.empty:
            raise HTTPException(status_code=404, detail="Lap data not found")
        
        fastest_lap1 = laps1.pick_fastest()
        fastest_lap2 = laps2.pick_fastest()
        
        telemetry1 = fastest_lap1.get_telemetry()
        telemetry2 = fastest_lap2.get_telemetry()
        
        if format == "json":
            if not PLOTLY_AVAILABLE:
                raise HTTPException(status_code=503, detail="Plotly not installed")
            
            fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=('Speed', 'Throttle', 'Brake'),
                vertical_spacing=0.08,
                shared_xaxes=True
            )
            
            # Speed traces
            fig.add_trace(go.Scatter(
                x=telemetry1['Distance'], y=telemetry1['Speed'],
                mode='lines', name=driver1, legendgroup='driver1',
                line=dict(color=TEAM_COLORS["default_primary"], width=2)
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=telemetry2['Distance'], y=telemetry2['Speed'],
                mode='lines', name=driver2, legendgroup='driver2',
                line=dict(color=TEAM_COLORS["default_secondary"], width=2)
            ), row=1, col=1)
            
            # Throttle traces
            fig.add_trace(go.Scatter(
                x=telemetry1['Distance'], y=telemetry1['Throttle'],
                mode='lines', name=driver1, legendgroup='driver1',
                line=dict(color=TEAM_COLORS["default_primary"], width=2),
                showlegend=False
            ), row=2, col=1)
            
            fig.add_trace(go.Scatter(
                x=telemetry2['Distance'], y=telemetry2['Throttle'],
                mode='lines', name=driver2, legendgroup='driver2',
                line=dict(color=TEAM_COLORS["default_secondary"], width=2),
                showlegend=False
            ), row=2, col=1)
            
            # Brake traces
            fig.add_trace(go.Scatter(
                x=telemetry1['Distance'], y=telemetry1['Brake'],
                mode='lines', name=driver1, legendgroup='driver1',
                line=dict(color=TEAM_COLORS["default_primary"], width=2),
                showlegend=False
            ), row=3, col=1)
            
            fig.add_trace(go.Scatter(
                x=telemetry2['Distance'], y=telemetry2['Brake'],
                mode='lines', name=driver2, legendgroup='driver2',
                line=dict(color=TEAM_COLORS["default_secondary"], width=2),
                showlegend=False
            ), row=3, col=1)
            
            # Update axes
            fig.update_xaxes(title_text="Distance (m)", row=3, col=1)
            fig.update_yaxes(title_text="Speed (km/h)", row=1, col=1)
            fig.update_yaxes(title_text="Throttle (%)", row=2, col=1)
            fig.update_yaxes(title_text="Brake", row=3, col=1)
            
            fig.update_layout(
                title=f'Throttle & Brake Analysis: {driver1} vs {driver2}<br>{year} {event} - {session}',
                height=800,
                template='plotly_white',
                hovermode='x unified'
            )
            
            return {
                "plotly_json": fig.to_json(),
                "type": "plotly"
            }
        
        else:  # PNG format
            if not MATPLOTLIB_AVAILABLE:
                raise HTTPException(status_code=503, detail="Matplotlib not installed")
            
            fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
            
            # Speed
            axes[0].plot(telemetry1['Distance'], telemetry1['Speed'], 
                        color=TEAM_COLORS["default_primary"], linewidth=2, label=driver1)
            axes[0].plot(telemetry2['Distance'], telemetry2['Speed'], 
                        color=TEAM_COLORS["default_secondary"], linewidth=2, label=driver2)
            axes[0].set_ylabel('Speed (km/h)', fontsize=11)
            axes[0].set_title(f'Throttle & Brake Analysis: {driver1} vs {driver2}\n{year} {event} - {session}', 
                             fontsize=13, fontweight='bold')
            axes[0].legend(loc='best')
            axes[0].grid(True, alpha=0.3)
            
            # Throttle
            axes[1].plot(telemetry1['Distance'], telemetry1['Throttle'], 
                        color=TEAM_COLORS["default_primary"], linewidth=2, label=driver1)
            axes[1].plot(telemetry2['Distance'], telemetry2['Throttle'], 
                        color=TEAM_COLORS["default_secondary"], linewidth=2, label=driver2)
            axes[1].set_ylabel('Throttle (%)', fontsize=11)
            axes[1].grid(True, alpha=0.3)
            
            # Brake
            axes[2].plot(telemetry1['Distance'], telemetry1['Brake'], 
                        color=TEAM_COLORS["default_primary"], linewidth=2, label=driver1)
            axes[2].plot(telemetry2['Distance'], telemetry2['Brake'], 
                        color=TEAM_COLORS["default_secondary"], linewidth=2, label=driver2)
            axes[2].set_xlabel('Distance (m)', fontsize=11)
            axes[2].set_ylabel('Brake', fontsize=11)
            axes[2].grid(True, alpha=0.3)
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error generating throttle-brake analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lap-time-distribution")
async def get_lap_time_distribution(
    year: int = Query(..., description="Season year"),
    event: str = Query(..., description="Event name"),
    session: str = Query(..., description="Session type"),
    drivers: str = Query(..., description="Comma-separated driver codes (e.g., 'VER,LEC,HAM')"),
    format: Literal["json", "png"] = Query("json", description="Output format")
):
    """
    Show lap time distribution for multiple drivers using box plots.
    Helps identify consistency and outliers.
    """
    try:
        driver_list = [d.strip() for d in drivers.split(',')]
        client = FastF1Client()
        
        session_data = client.get_session(year, event, session)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        lap_times = {}
        for driver in driver_list:
            laps = client.get_driver_laps(year, event, session, driver)
            if not laps.empty:
                # Convert lap times to seconds
                valid_laps = laps[laps['LapTime'].notna()]
                times = []
                for lt in valid_laps['LapTime']:
                    # Handle both timedelta and numeric types
                    if hasattr(lt, 'total_seconds'):
                        times.append(lt.total_seconds())
                    elif isinstance(lt, (int, float)):
                        times.append(float(lt))
                    else:
                        # Try to convert string to float
                        try:
                            times.append(float(lt))
                        except:
                            continue
                if times:
                    lap_times[driver] = times
        
        if not lap_times:
            raise HTTPException(status_code=404, detail="No lap data found for specified drivers")
        
        if format == "json":
            if not PLOTLY_AVAILABLE:
                raise HTTPException(status_code=503, detail="Plotly not installed")
            
            fig = go.Figure()
            
            for driver, times in lap_times.items():
                fig.add_trace(go.Box(
                    y=times,
                    name=driver,
                    boxmean='sd'
                ))
            
            fig.update_layout(
                title=f'Lap Time Distribution<br>{year} {event} - {session}',
                yaxis_title='Lap Time (seconds)',
                template='plotly_white',
                height=500,
                showlegend=True
            )
            
            return {
                "plotly_json": fig.to_json(),
                "type": "plotly"
            }
        
        else:  # PNG format
            if not MATPLOTLIB_AVAILABLE:
                raise HTTPException(status_code=503, detail="Matplotlib not installed")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            positions = list(range(1, len(lap_times) + 1))
            data = [times for times in lap_times.values()]
            labels = list(lap_times.keys())
            
            bp = ax.boxplot(data, positions=positions, labels=labels, patch_artist=True)
            
            # Color boxes
            for patch in bp['boxes']:
                patch.set_facecolor('#0600EF')
                patch.set_alpha(0.6)
            
            ax.set_ylabel('Lap Time (seconds)', fontsize=12)
            ax.set_title(f'Lap Time Distribution\n{year} {event} - {session}', 
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error generating lap time distribution: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sector-comparison")
async def get_sector_comparison(
    year: int = Query(..., description="Season year"),
    event: str = Query(..., description="Event name"),
    session: str = Query(..., description="Session type"),
    driver1: str = Query(..., description="First driver code"),
    driver2: str = Query(..., description="Second driver code"),
    format: Literal["json", "png"] = Query("json", description="Output format")
):
    """
    Compare sector times between two drivers on their fastest laps.
    Shows which driver is faster in each sector.
    """
    try:
        client = FastF1Client()
        
        session_data = client.get_session(year, event, session)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        laps1 = client.get_driver_laps(year, event, session, driver1)
        laps2 = client.get_driver_laps(year, event, session, driver2)
        
        if laps1.empty or laps2.empty:
            raise HTTPException(status_code=404, detail="Lap data not found")
        
        fastest_lap1 = laps1.pick_fastest()
        fastest_lap2 = laps2.pick_fastest()
        
        # Extract sector times
        sectors1 = [
            fastest_lap1['Sector1Time'].total_seconds() if fastest_lap1['Sector1Time'] else 0,
            fastest_lap1['Sector2Time'].total_seconds() if fastest_lap1['Sector2Time'] else 0,
            fastest_lap1['Sector3Time'].total_seconds() if fastest_lap1['Sector3Time'] else 0
        ]
        
        sectors2 = [
            fastest_lap2['Sector1Time'].total_seconds() if fastest_lap2['Sector1Time'] else 0,
            fastest_lap2['Sector2Time'].total_seconds() if fastest_lap2['Sector2Time'] else 0,
            fastest_lap2['Sector3Time'].total_seconds() if fastest_lap2['Sector3Time'] else 0
        ]
        
        sector_names = ['Sector 1', 'Sector 2', 'Sector 3']
        
        if format == "json":
            if not PLOTLY_AVAILABLE:
                raise HTTPException(status_code=503, detail="Plotly not installed")
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=sector_names,
                y=sectors1,
                name=driver1,
                marker_color=TEAM_COLORS["default_primary"]
            ))
            
            fig.add_trace(go.Bar(
                x=sector_names,
                y=sectors2,
                name=driver2,
                marker_color=TEAM_COLORS["default_secondary"]
            ))
            
            fig.update_layout(
                title=f'Sector Comparison: {driver1} vs {driver2}<br>{year} {event} - {session}',
                yaxis_title='Time (seconds)',
                barmode='group',
                template='plotly_white',
                height=500
            )
            
            return {
                "plotly_json": fig.to_json(),
                "type": "plotly"
            }
        
        else:  # PNG format
            if not MATPLOTLIB_AVAILABLE:
                raise HTTPException(status_code=503, detail="Matplotlib not installed")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            x = range(len(sector_names))
            width = 0.35
            
            ax.bar([i - width/2 for i in x], sectors1, width, 
                  label=driver1, color=TEAM_COLORS["default_primary"])
            ax.bar([i + width/2 for i in x], sectors2, width, 
                  label=driver2, color=TEAM_COLORS["default_secondary"])
            
            ax.set_xlabel('Sectors', fontsize=12)
            ax.set_ylabel('Time (seconds)', fontsize=12)
            ax.set_title(f'Sector Comparison: {driver1} vs {driver2}\n{year} {event} - {session}', 
                        fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(sector_names)
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error generating sector comparison: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tyre-degradation")
async def get_tyre_degradation(
    year: int = Query(..., description="Season year"),
    event: str = Query(..., description="Event name"),
    session: str = Query(..., description="Session type (typically 'R' for race)"),
    driver: str = Query(..., description="Driver code"),
    format: Literal["json", "png"] = Query("json", description="Output format")
):
    """
    Visualize tyre degradation by plotting lap times against tyre age.
    Different compounds shown in different colors.
    """
    try:
        client = FastF1Client()
        
        session_data = client.get_session(year, event, session)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        laps = client.get_driver_laps(year, event, session, driver)
        
        if laps.empty:
            raise HTTPException(status_code=404, detail="No lap data found")
        
        # Filter valid laps
        valid_laps = laps[laps['LapTime'].notna() & laps['Compound'].notna()]
        
        if valid_laps.empty:
            raise HTTPException(status_code=404, detail="No valid tyre data found")
        
        # Group by compound
        compounds = valid_laps['Compound'].unique()
        
        if format == "json":
            if not PLOTLY_AVAILABLE:
                raise HTTPException(status_code=503, detail="Plotly not installed")
            
            fig = go.Figure()
            
            compound_colors = {
                'SOFT': '#FF0000',
                'MEDIUM': '#FFFF00',
                'HARD': '#FFFFFF',
                'INTERMEDIATE': '#00FF00',
                'WET': '#0000FF'
            }
            
            for compound in compounds:
                compound_laps = valid_laps[valid_laps['Compound'] == compound]
                lap_times = [lt.total_seconds() for lt in compound_laps['LapTime']]
                tyre_life = compound_laps['TyreLife'].tolist()
                
                fig.add_trace(go.Scatter(
                    x=tyre_life,
                    y=lap_times,
                    mode='lines+markers',
                    name=compound,
                    line=dict(color=compound_colors.get(compound, '#999999'), width=2)
                ))
            
            fig.update_layout(
                title=f'Tyre Degradation: {driver}<br>{year} {event} - {session}',
                xaxis_title='Tyre Life (laps)',
                yaxis_title='Lap Time (seconds)',
                template='plotly_white',
                height=500,
                hovermode='closest'
            )
            
            return {
                "plotly_json": fig.to_json(),
                "type": "plotly"
            }
        
        else:  # PNG format
            if not MATPLOTLIB_AVAILABLE:
                raise HTTPException(status_code=503, detail="Matplotlib not installed")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            compound_colors = {
                'SOFT': 'red',
                'MEDIUM': 'yellow',
                'HARD': 'white',
                'INTERMEDIATE': 'green',
                'WET': 'blue'
            }
            
            for compound in compounds:
                compound_laps = valid_laps[valid_laps['Compound'] == compound]
                lap_times = [lt.total_seconds() for lt in compound_laps['LapTime']]
                tyre_life = compound_laps['TyreLife'].tolist()
                
                color = compound_colors.get(compound, 'gray')
                ax.plot(tyre_life, lap_times, marker='o', linewidth=2, 
                       label=compound, color=color, markersize=4)
            
            ax.set_xlabel('Tyre Life (laps)', fontsize=12)
            ax.set_ylabel('Lap Time (seconds)', fontsize=12)
            ax.set_title(f'Tyre Degradation: {driver}\n{year} {event} - {session}', 
                        fontsize=14, fontweight='bold')
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error generating tyre degradation chart: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gear-usage")
async def get_gear_usage(
    year: int = Query(..., description="Season year"),
    event: str = Query(..., description="Event name"),
    session: str = Query(..., description="Session type"),
    driver: str = Query(..., description="Driver code"),
    format: Literal["json", "png"] = Query("json", description="Output format")
):
    """
    Visualize gear changes throughout a lap.
    Shows which gear is used at each point on track.
    """
    try:
        client = FastF1Client()
        
        session_data = client.get_session(year, event, session)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        laps = client.get_driver_laps(year, event, session, driver)
        
        if laps.empty:
            raise HTTPException(status_code=404, detail="No lap data found")
        
        # Get fastest lap properly
        fastest_lap = laps.pick_fastest()
        telemetry = fastest_lap.get_telemetry()
        
        if telemetry.empty or 'nGear' not in telemetry.columns:
            raise HTTPException(status_code=404, detail="Gear telemetry not available")
        
        if format == "json":
            if not PLOTLY_AVAILABLE:
                raise HTTPException(status_code=503, detail="Plotly not installed")
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=telemetry['Distance'],
                y=telemetry['nGear'],
                mode='lines',
                line=dict(color=TEAM_COLORS["default_primary"], width=2),
                fill='tozeroy',
                name='Gear'
            ))
            
            fig.update_layout(
                title=f'Gear Usage: {driver}<br>{year} {event} - {session} (Fastest Lap)',
                xaxis_title='Distance (m)',
                yaxis_title='Gear',
                template='plotly_white',
                height=500,
                yaxis=dict(dtick=1)
            )
            
            return {
                "plotly_json": fig.to_json(),
                "type": "plotly"
            }
        
        else:  # PNG format
            if not MATPLOTLIB_AVAILABLE:
                raise HTTPException(status_code=503, detail="Matplotlib not installed")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ax.plot(telemetry['Distance'], telemetry['nGear'], 
                   color=TEAM_COLORS["default_primary"], linewidth=2)
            ax.fill_between(telemetry['Distance'], telemetry['nGear'], 
                           alpha=0.3, color=TEAM_COLORS["default_primary"])
            
            ax.set_xlabel('Distance (m)', fontsize=12)
            ax.set_ylabel('Gear', fontsize=12)
            ax.set_title(f'Gear Usage: {driver}\n{year} {event} - {session} (Fastest Lap)', 
                        fontsize=14, fontweight='bold')
            ax.set_yticks(range(1, 9))
            ax.grid(True, alpha=0.3)
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error generating gear usage chart: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance-radar")
async def get_performance_radar(
    year: int = Query(..., description="Season year"),
    event: str = Query(..., description="Event name"),
    session: str = Query(..., description="Session type"),
    driver1: str = Query(..., description="First driver code"),
    driver2: str = Query(..., description="Second driver code"),
    format: Literal["json", "png"] = Query("json", description="Output format")
):
    """
    Create a radar chart comparing multiple performance metrics:
    - Top Speed
    - Consistency (inverse of lap time std dev)
    - Braking Performance
    - Cornering Speed
    - Throttle Application
    """
    try:
        client = FastF1Client()
        
        session_data = client.get_session(year, event, session)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        laps1 = client.get_driver_laps(year, event, session, driver1)
        laps2 = client.get_driver_laps(year, event, session, driver2)
        
        if laps1.empty or laps2.empty:
            raise HTTPException(status_code=404, detail="Lap data not found")
        
        # Calculate metrics for both drivers
        def calculate_metrics(laps):
            fastest_lap = laps.pick_fastest()
            telemetry = fastest_lap.get_telemetry()
            
            if telemetry.empty:
                return None
            
            # Normalize to 0-100 scale
            metrics = {
                'Top Speed': min(telemetry['Speed'].max() / 350 * 100, 100),
                'Consistency': min(100 - (laps['LapTime'].std().total_seconds() * 10), 100),
                'Braking': min(telemetry['Brake'].sum() / len(telemetry) * 100, 100),
                'Cornering': min(telemetry[telemetry['Speed'] < 150]['Speed'].mean() / 150 * 100, 100) if len(telemetry[telemetry['Speed'] < 150]) > 0 else 50,
                'Throttle': min(telemetry['Throttle'].mean(), 100)
            }
            return metrics
        
        metrics1 = calculate_metrics(laps1)
        metrics2 = calculate_metrics(laps2)
        
        if not metrics1 or not metrics2:
            raise HTTPException(status_code=404, detail="Unable to calculate performance metrics")
        
        categories = list(metrics1.keys())
        
        if format == "json":
            if not PLOTLY_AVAILABLE:
                raise HTTPException(status_code=503, detail="Plotly not installed")
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=list(metrics1.values()),
                theta=categories,
                fill='toself',
                name=driver1,
                line=dict(color=TEAM_COLORS["default_primary"], width=2)
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=list(metrics2.values()),
                theta=categories,
                fill='toself',
                name=driver2,
                line=dict(color=TEAM_COLORS["default_secondary"], width=2)
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title=f'Performance Radar: {driver1} vs {driver2}<br>{year} {event} - {session}',
                showlegend=True,
                template='plotly_white',
                height=600
            )
            
            return {
                "plotly_json": fig.to_json(),
                "type": "plotly"
            }
        
        else:  # PNG format
            if not MATPLOTLIB_AVAILABLE:
                raise HTTPException(status_code=503, detail="Matplotlib not installed")
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            
            angles = [i * 2 * 3.14159 / len(categories) for i in range(len(categories))]
            values1 = list(metrics1.values())
            values2 = list(metrics2.values())
            
            # Close the plot
            angles += angles[:1]
            values1 += values1[:1]
            values2 += values2[:1]
            
            ax.plot(angles, values1, 'o-', linewidth=2, 
                   label=driver1, color=TEAM_COLORS["default_primary"])
            ax.fill(angles, values1, alpha=0.25, color=TEAM_COLORS["default_primary"])
            
            ax.plot(angles, values2, 'o-', linewidth=2, 
                   label=driver2, color=TEAM_COLORS["default_secondary"])
            ax.fill(angles, values2, alpha=0.25, color=TEAM_COLORS["default_secondary"])
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_ylim(0, 100)
            ax.set_title(f'Performance Radar: {driver1} vs {driver2}\n{year} {event} - {session}', 
                        fontsize=14, fontweight='bold', pad=20)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            ax.grid(True)
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            buf.seek(0)
            
            return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        logger.error(f"Error generating performance radar: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def visualization_health():
    """
    Check if visualization libraries are properly installed.
    """
    return {
        "status": "ok",
        "libraries": {
            "plotly": PLOTLY_AVAILABLE,
            "matplotlib": MATPLOTLIB_AVAILABLE
        },
        "capabilities": {
            "json_charts": PLOTLY_AVAILABLE,
            "png_images": MATPLOTLIB_AVAILABLE
        }
    }
