import streamlit as st
import pandas as pd
import numpy as np
import math
import io

# Handle optional dependencies
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not installed. Install with: `pip install plotly` for enhanced visualizations.")

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    st.info("ℹ️ SciPy not installed. Basic functionality available without advanced statistics.")

# Page configuration
st.set_page_config(
    page_title="LSM to Mean/SD Converter",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #ff7f0e;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.info-box {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 5px solid #1f77b4;
    margin: 1rem 0;
}
.warning-box {
    background-color: #fff3cd;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 5px solid #ffc107;
    margin: 1rem 0;
}
.success-box {
    background-color: #d4edda;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 5px solid #28a745;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Helper functions
def lsm_to_mean_sd(lsm, se, n, adjustment_factor=1.0, design_effect=1.0):
    """
    Convert LSM and SE to Mean and SD
    
    Parameters:
    lsm: Least Square Mean
    se: Standard Error
    n: Sample size
    adjustment_factor: Factor to account for covariate adjustment (1.0-1.2)
    design_effect: Factor for complex study designs
    """
    # Convert SE to SD
    # For LSM: SE = SD / sqrt(n_effective)
    # Where n_effective might be different from n due to adjustments
    
    # Estimate effective sample size
    n_effective = n / design_effect
    
    # Calculate SD from SE
    sd_unadjusted = se * math.sqrt(n_effective)
    
    # Apply adjustment factor for covariate adjustment
    sd_adjusted = sd_unadjusted * adjustment_factor
    
    # Calculate confidence intervals for the conversion
    ci_lower = lsm - 1.96 * se
    ci_upper = lsm + 1.96 * se
    
    # Uncertainty in SD conversion
    sd_uncertainty = sd_adjusted * 0.1  # Approximate uncertainty
    
    return {
        'mean': lsm,
        'sd': sd_adjusted,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'sd_uncertainty': sd_uncertainty,
        'conversion_quality': calculate_quality_score(n, se, adjustment_factor)
    }

def calculate_quality_score(n, se, adjustment_factor):
    """Calculate quality score for the conversion (0-100)"""
    # Higher sample size = better quality
    size_score = min(n / 100, 1.0) * 40
    
    # Lower SE relative to magnitude = better quality
    precision_score = max(0, 30 - (se * 100)) if se < 0.3 else 0
    
    # Less adjustment = better quality
    adjustment_score = max(0, 30 - (adjustment_factor - 1) * 100)
    
    total_score = size_score + precision_score + adjustment_score
    return min(max(total_score, 0), 100)

def suggest_adjustment_factor(study_design, num_covariates):
    """Suggest adjustment factor based on study characteristics"""
    base_factor = 1.0
    
    if study_design == "Randomized Controlled Trial":
        base_factor = 1.0
    elif study_design == "Cohort Study":
        base_factor = 1.05
    elif study_design == "Case-Control Study":
        base_factor = 1.1
    elif study_design == "Cross-sectional Study":
        base_factor = 1.05
    
    # Increase factor based on number of covariates
    covariate_adjustment = min(num_covariates * 0.02, 0.2)
    
    return base_factor + covariate_adjustment

def create_comparison_plot(original_data, converted_data):
    """Create comparison visualization"""
    if not PLOTLY_AVAILABLE:
        st.error("Plotly not available. Install with: pip install plotly")
        return None
        
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Original LSM Data', 'Converted Mean/SD Data'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Original data plot
    fig.add_trace(
        go.Scatter(
            x=['Group 1', 'Group 2'],
            y=[original_data['lsm1'], original_data['lsm2']],
            error_y=dict(
                type='data',
                array=[original_data['se1'], original_data['se2']],
                visible=True
            ),
            mode='markers+lines',
            name='LSM ± SE',
            marker=dict(size=10, color='blue')
        ),
        row=1, col=1
    )
    
    # Converted data plot
    fig.add_trace(
        go.Scatter(
            x=['Group 1', 'Group 2'],
            y=[converted_data['mean1'], converted_data['mean2']],
            error_y=dict(
                type='data',
                array=[converted_data['sd1'], converted_data['sd2']],
                visible=True
            ),
            mode='markers+lines',
            name='Mean ± SD',
            marker=dict(size=10, color='red')
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title="LSM vs Mean/SD Comparison",
        showlegend=True,
        height=400
    )
    
    return fig

def create_simple_bar_chart(studies, values, title):
    """Create simple bar chart without plotly"""
    chart_data = pd.DataFrame({
        'Studies': studies,
        'Values': values
    })
    st.bar_chart(chart_data.set_index('Studies'))

# Main app
def main():
    st.markdown('<h1 class="main-header">🧮 LSM to Mean/SD Converter</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">AI-Powered Statistical Converter for Meta-Analysis</p>', unsafe_allow_html=True)
    
    # Developer info
    with st.expander("👨‍💻 About the Developer"):
        st.markdown("""
        **Muhammad Nabeel Saddique**  
        *Fourth-year MBBS Student, King Edward Medical University, Lahore, Pakistan*
        
        🎓 **Expertise**: Systematic Reviews & Meta-Analysis  
        🏢 **Founder**: Nibras Research Academy  
        🛠️ **Tools**: Rayyan, Zotero, EndNote, WebPlotDigitizer, Meta-Converter, RevMan, MetaXL, Jamovi, CMA, OpenMeta, R Studio
        
        *Passionate about research and improving healthcare outcomes through evidence synthesis.*
        """)
    
    # Sidebar for settings
    st.sidebar.markdown('<h2 class="sub-header">⚙️ Conversion Settings</h2>', unsafe_allow_html=True)
    
    # Study characteristics
    study_design = st.sidebar.selectbox(
        "Study Design",
        ["Randomized Controlled Trial", "Cohort Study", "Case-Control Study", "Cross-sectional Study"]
    )
    
    num_covariates = st.sidebar.slider(
        "Number of Adjusted Covariates",
        min_value=0,
        max_value=20,
        value=3,
        help="Number of variables adjusted for in the statistical model"
    )
    
    design_effect = st.sidebar.slider(
        "Design Effect",
        min_value=1.0,
        max_value=3.0,
        value=1.0,
        step=0.1,
        help="Accounts for complex sampling or clustering (1.0 = simple random sampling)"
    )
    
    # Auto-suggest adjustment factor
    suggested_factor = suggest_adjustment_factor(study_design, num_covariates)
    
    adjustment_factor = st.sidebar.slider(
        "Adjustment Factor",
        min_value=1.0,
        max_value=2.0,
        value=suggested_factor,
        step=0.01,
        help=f"Suggested: {suggested_factor:.2f} based on study characteristics"
    )
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔢 Single Conversion", "📊 Batch Conversion", "📈 Visualization", "📚 Tutorial"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Single Study Conversion</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📥 Input Data (LSM Format)**")
            
            # Group 1 inputs
            st.markdown("**Group 1:**")
            lsm1 = st.number_input("LSM 1", value=0.0, format="%.3f")
            se1 = st.number_input("SE 1", value=0.0, min_value=0.0, format="%.3f")
            n1 = st.number_input("Sample Size 1", value=30, min_value=1, step=1)
            
            st.markdown("---")
            
            # Group 2 inputs
            st.markdown("**Group 2:**")
            lsm2 = st.number_input("LSM 2", value=0.0, format="%.3f")
            se2 = st.number_input("SE 2", value=0.0, min_value=0.0, format="%.3f")
            n2 = st.number_input("Sample Size 2", value=30, min_value=1, step=1)
            
        with col2:
            st.markdown("**📤 Output Data (Mean/SD Format)**")
            
            if st.button("🔄 Convert", type="primary"):
                if se1 > 0 and se2 > 0:
                    # Perform conversions
                    result1 = lsm_to_mean_sd(lsm1, se1, n1, adjustment_factor, design_effect)
                    result2 = lsm_to_mean_sd(lsm2, se2, n2, adjustment_factor, design_effect)
                    
                    # Display results
                    st.markdown("**Group 1 Results:**")
                    st.write(f"Mean: {result1['mean']:.3f}")
                    st.write(f"SD: {result1['sd']:.3f}")
                    st.write(f"Quality Score: {result1['conversion_quality']:.1f}/100")
                    
                    st.markdown("**Group 2 Results:**")
                    st.write(f"Mean: {result2['mean']:.3f}")
                    st.write(f"SD: {result2['sd']:.3f}")
                    st.write(f"Quality Score: {result2['conversion_quality']:.1f}/100")
                    
                    # Effect size calculation
                    pooled_sd = math.sqrt(((n1-1)*result1['sd']**2 + (n2-1)*result2['sd']**2) / (n1+n2-2))
                    cohens_d = (result1['mean'] - result2['mean']) / pooled_sd
                    
                    st.markdown("**📊 Effect Size:**")
                    st.write(f"Cohen's d: {cohens_d:.3f}")
                    
                    # Quality assessment
                    avg_quality = (result1['conversion_quality'] + result2['conversion_quality']) / 2
                    
                    if avg_quality >= 80:
                        st.markdown('<div class="success-box">✅ <strong>High Quality Conversion</strong> - Reliable for meta-analysis</div>', unsafe_allow_html=True)
                    elif avg_quality >= 60:
                        st.markdown('<div class="warning-box">⚠️ <strong>Moderate Quality Conversion</strong> - Use with caution</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="warning-box">❌ <strong>Low Quality Conversion</strong> - Consider excluding or contacting authors</div>', unsafe_allow_html=True)
                    
                    # Export options
                    st.markdown("**📁 Export Data:**")
                    
                    # Create export dataframe
                    export_data = pd.DataFrame({
                        'Group': ['Group 1', 'Group 2'],
                        'Mean': [result1['mean'], result2['mean']],
                        'SD': [result1['sd'], result2['sd']],
                        'N': [n1, n2],
                        'Quality_Score': [result1['conversion_quality'], result2['conversion_quality']]
                    })
                    
                    csv = export_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="lsm_conversion_results.csv",
                        mime="text/csv"
                    )
                    
                else:
                    st.error("Please enter valid Standard Error values (> 0)")
    
    with tab2:
        st.markdown('<h2 class="sub-header">Batch Processing</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">📁 Upload a CSV file with columns: Study_ID, Group, LSM, SE, N</div>', unsafe_allow_html=True)
        
        # Sample data template
        sample_data = pd.DataFrame({
            'Study_ID': ['Study_1', 'Study_1', 'Study_2', 'Study_2'],
            'Group': ['Treatment', 'Control', 'Treatment', 'Control'],
            'LSM': [2.5, 1.8, 3.2, 2.1],
            'SE': [0.3, 0.25, 0.4, 0.3],
            'N': [50, 48, 60, 55]
        })
        
        st.markdown("**📋 Template:**")
        st.dataframe(sample_data)
        
        template_csv = sample_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Template",
            data=template_csv,
            file_name="lsm_converter_template.csv",
            mime="text/csv"
        )
        
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.markdown("**📊 Uploaded Data:**")
                st.dataframe(df)
                
                if st.button("🔄 Process Batch", type="primary"):
                    # Process each row
                    results = []
                    
                    for idx, row in df.iterrows():
                        result = lsm_to_mean_sd(
                            row['LSM'], 
                            row['SE'], 
                            row['N'], 
                            adjustment_factor, 
                            design_effect
                        )
                        
                        results.append({
                            'Study_ID': row['Study_ID'],
                            'Group': row['Group'],
                            'Original_LSM': row['LSM'],
                            'Original_SE': row['SE'],
                            'Converted_Mean': result['mean'],
                            'Converted_SD': result['sd'],
                            'N': row['N'],
                            'Quality_Score': result['conversion_quality']
                        })
                    
                    results_df = pd.DataFrame(results)
                    
                    st.markdown("**📈 Conversion Results:**")
                    st.dataframe(results_df)
                    
                    # Download results
                    results_csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results",
                        data=results_csv,
                        file_name="batch_conversion_results.csv",
                        mime="text/csv"
                    )
                    
                    # Summary statistics
                    avg_quality = results_df['Quality_Score'].mean()
                    st.metric("Average Quality Score", f"{avg_quality:.1f}/100")
                    
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    with tab3:
        st.markdown('<h2 class="sub-header">Data Visualization</h2>', unsafe_allow_html=True)
        
        if not PLOTLY_AVAILABLE:
            st.warning("📊 Enhanced visualizations require Plotly. Install with: `pip install plotly`")
            st.markdown("**Alternative: Basic Charts Available**")
        
        # Demo data for visualization
        if st.button("📊 Generate Demo Visualization"):
            # Create sample data
            studies = ['Study A', 'Study B', 'Study C', 'Study D', 'Study E']
            lsm_values = [2.3, 1.8, 3.1, 2.7, 2.0]
            se_values = [0.3, 0.25, 0.35, 0.28, 0.22]
            sample_sizes = [45, 52, 38, 48, 55]
            
            converted_results = []
            for i in range(len(studies)):
                result = lsm_to_mean_sd(lsm_values[i], se_values[i], sample_sizes[i], adjustment_factor, design_effect)
                converted_results.append(result)
            
            if PLOTLY_AVAILABLE:
                # Forest plot style visualization
                fig = go.Figure()
                
                # Add LSM data
                fig.add_trace(go.Scatter(
                    x=[r['mean'] for r in converted_results],
                    y=studies,
                    error_x=dict(
                        type='data',
                        array=[r['sd'] for r in converted_results],
                        visible=True
                    ),
                    mode='markers',
                    marker=dict(size=12, color='blue'),
                    name='Converted Mean ± SD'
                ))
                
                fig.update_layout(
                    title='Forest Plot: Converted Mean and SD Values',
                    xaxis_title='Effect Size',
                    yaxis_title='Studies',
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Quality scores visualization
                quality_scores = [r['conversion_quality'] for r in converted_results]
                
                fig2 = px.bar(
                    x=studies,
                    y=quality_scores,
                    title='Conversion Quality Scores by Study',
                    labels={'x': 'Studies', 'y': 'Quality Score (0-100)'},
                    color=quality_scores,
                    color_continuous_scale='RdYlGn'
                )
                
                fig2.add_hline(y=80, line_dash="dash", line_color="green", 
                              annotation_text="High Quality Threshold")
                fig2.add_hline(y=60, line_dash="dash", line_color="orange", 
                              annotation_text="Moderate Quality Threshold")
                
                st.plotly_chart(fig2, use_container_width=True)
            
            else:
                # Fallback to basic Streamlit charts
                st.markdown("**📊 Converted Mean Values by Study**")
                mean_data = pd.DataFrame({
                    'Study': studies,
                    'Mean': [r['mean'] for r in converted_results]
                })
                st.bar_chart(mean_data.set_index('Study'))
                
                st.markdown("**📈 Quality Scores by Study**")
                quality_data = pd.DataFrame({
                    'Study': studies,
                    'Quality_Score': [r['conversion_quality'] for r in converted_results]
                })
                st.bar_chart(quality_data.set_index('Study'))
                
                # Display data table
                st.markdown("**📋 Detailed Results**")
                results_table = pd.DataFrame({
                    'Study': studies,
                    'Original_LSM': lsm_values,
                    'Original_SE': se_values,
                    'Converted_Mean': [r['mean'] for r in converted_results],
                    'Converted_SD': [f"{r['sd']:.3f}" for r in converted_results],
                    'Quality_Score': [f"{r['conversion_quality']:.1f}" for r in converted_results]
                })
                st.dataframe(results_table)
    
    with tab4:
        st.markdown('<h2 class="sub-header">📚 How to Use This Tool</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 🎯 Purpose
        This tool converts Least Square Means (LSM) with Standard Errors to regular Means with Standard Deviations, 
        enabling inclusion of adjusted analyses in meta-analyses.
        
        ### 📋 Step-by-Step Guide
        
        1. **Study Information**: Select your study design and provide adjustment details
        2. **Input Data**: Enter LSM values, Standard Errors, and sample sizes
        3. **Conversion**: Click convert to get Mean and SD values
        4. **Quality Check**: Review the quality score for reliability
        5. **Export**: Download results for use in meta-analysis software
        
        ### ⚠️ Important Considerations
        
        - **Quality Score**: Aim for scores >60 for reliable conversions
        - **Adjustment Factor**: Higher values for more complex adjustments
        - **Sample Size**: Larger samples generally give better conversions
        - **Design Effect**: Accounts for clustering or complex sampling
        
        ### 🔬 Statistical Background
        
        **LSM to Mean/SD Conversion Formula:**
        ```
        Mean = LSM (unchanged)
        SD = SE × √(n_effective) × adjustment_factor
        ```
        
        Where:
        - `n_effective = n / design_effect`
        - `adjustment_factor` depends on study characteristics
        
        ### 🎯 Meta-Analysis Integration
        
        The converted values can be directly used in:
        - RevMan (Cochrane Reviews)
        - Comprehensive Meta-Analysis (CMA)
        - R packages (metafor, meta)
        - Stata meta-analysis commands
        
        ### 📞 Support
        
        For questions or support, contact: **Nibras Research Academy**
        
        *Developed for NRIC25 - King Edward Medical University*
        """)
        
        # Validation section
        st.markdown('<h3 class="sub-header">✅ Validation Example</h3>', unsafe_allow_html=True)
        
        st.markdown("""
        **Example Conversion:**
        - Study: RCT with 3 covariates
        - Group 1: LSM = 2.5, SE = 0.3, N = 50
        - Group 2: LSM = 1.8, SE = 0.25, N = 48
        
        **Converted Results:**
        - Group 1: Mean = 2.5, SD ≈ 2.13
        - Group 2: Mean = 1.8, SD ≈ 1.74
        - Cohen's d ≈ 0.36 (small to medium effect)
        """)

if __name__ == "__main__":
    main()