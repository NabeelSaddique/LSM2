# 🧮 LSM to Mean/SD Converter

**AI-Powered Statistical Converter for Meta-Analysis**

---

## 📋 Project Overview

### **Problem Statement**
Many clinical trials report Least Square Means (LSM) with Standard Errors instead of simple means and standard deviations. This creates a major barrier for meta-analysis inclusion, as most meta-analysis software requires mean ± SD format. Medical students and researchers often exclude valuable studies or make incorrect conversions, leading to biased evidence synthesis.

### **Target Population**
- Medical students conducting systematic reviews
- Clinical researchers performing meta-analyses  
- Evidence synthesis teams in healthcare organizations
- Guideline development committees

### **AI Solution/Approach**
Web-based converter tool that intelligently transforms LSM data to mean/SD using context-aware algorithms, quality scoring, and uncertainty quantification.

---

## 👨‍💻 Developer Information

**Muhammad Nabeel Saddique**  
*Fourth-year MBBS Student, King Edward Medical University, Lahore, Pakistan*

🎓 **Expertise**: Systematic Reviews & Meta-Analysis  
🏢 **Founder**: Nibras Research Academy  
🛠️ **Research Tools**: Rayyan, Zotero, EndNote, WebPlotDigitizer, Meta-Converter, RevMan, MetaXL, Jamovi, Comprehensive Meta-Analysis (CMA), OpenMeta, R Studio

*Passionate about research and improving healthcare outcomes through evidence synthesis.*

---

## 🚀 Features

### **Core Functionality**
- ✅ **Single Study Conversion**: Convert individual LSM values with quality scoring
- ✅ **Batch Processing**: Upload CSV files for multiple studies at once
- ✅ **Smart Adjustment Factors**: Auto-suggest based on study design and covariates
- ✅ **Quality Assessment**: 0-100 scoring system for conversion reliability
- ✅ **Effect Size Calculation**: Automatic Cohen's d computation
- ✅ **Export Options**: Download results as CSV for meta-analysis software

### **Advanced Features**
- 📊 **Interactive Visualizations**: Forest plots and quality assessments (with Plotly)
- 🎯 **Context-Aware Conversion**: Considers study design, sample size, and adjustments
- ⚠️ **Uncertainty Quantification**: Provides confidence bounds for conversions
- 📈 **Statistical Validation**: Built-in quality checks and recommendations
- 🔄 **Meta-Analysis Integration**: Ready-to-use outputs for RevMan, R, Stata, CMA

---

## 📦 Installation

### **Basic Installation**
```bash
pip install streamlit pandas numpy
```

### **Full Installation (Recommended)**
```bash
pip install streamlit pandas numpy plotly scipy
```

### **Using Requirements File**
```bash
pip install -r requirements.txt
```

---

## 🖥️ Usage

### **Running the Application**
```bash
streamlit run lsm_converter.py
```

### **Step-by-Step Guide**

1. **📊 Single Study Conversion**
   - Enter LSM values, Standard Errors, and sample sizes
   - Select study design and adjustment parameters
   - Click "Convert" to get Mean and SD values
   - Review quality score for reliability assessment

2. **📁 Batch Processing**
   - Download the CSV template
   - Upload your data file with multiple studies
   - Process all conversions simultaneously
   - Export results for meta-analysis

3. **📈 Visualization**
   - Generate demo forest plots
   - View quality score distributions
   - Export publication-ready graphics

4. **📚 Tutorial**
   - Complete usage instructions
   - Statistical background and formulas
   - Integration with meta-analysis software

---

## 🔬 Technical Details

### **AI Task Performance**
- **Pattern Recognition**: Identify LSM vs mean reporting
- **Statistical Modeling**: Apply appropriate conversion algorithms
- **Uncertainty Estimation**: Quantify conversion reliability
- **Quality Control**: Flag problematic conversions

### **Data Types Used**
- LSM values and standard errors
- Sample sizes per group
- Study design information
- Baseline patient characteristics
- Number of adjusted covariates
- Correlation matrices (when available)

### **Conversion Algorithm**
```
Mean = LSM (unchanged)
SD = SE × √(n_effective) × adjustment_factor

Where:
- n_effective = n / design_effect
- adjustment_factor depends on study characteristics
```

### **Quality Scoring System**
- **Sample Size Component** (40 points): Larger samples = higher quality
- **Precision Component** (30 points): Lower SE relative to effect = better quality  
- **Adjustment Component** (30 points): Less adjustment = more reliable conversion
- **Total Score**: 0-100 scale with interpretation guidelines

---

## 📊 Real-Life Use Cases

### **Current Solutions vs. Our Tool**
- **Existing**: Manual approximations or study exclusion
- **Limited Tools**: Basic calculators without context consideration
- **Our Innovation**: Intelligent tool with study context and uncertainty estimates

### **Integration with Meta-Analysis Software**
- **RevMan**: Direct CSV import for Cochrane reviews
- **Comprehensive Meta-Analysis (CMA)**: Compatible data format
- **R packages**: Ready for metafor, meta packages
- **Stata**: Compatible with meta-analysis commands

---

## 📈 Success Measurement

### **Accuracy Metrics**
- Compare converted values to known mean/SD from validation studies
- Statistical agreement with manual expert conversions

### **Efficiency Metrics**
- Reduction in conversion time from hours to minutes
- Increased study inclusion rates in meta-analyses

### **User Adoption**
- Track usage by meta-analysis researchers
- Monitor citations of meta-analyses using the tool

### **Quality Impact**
- Improvement in effect size estimate accuracy
- Reduction in conversion-related errors

---

## 🔮 Future Potential

### **Short-term Enhancements**
- Integration with systematic review software (Covidence, DistillerSR)
- API development for automated workflows
- Mobile app version for field researchers

### **Long-term Vision**
- Machine learning from user feedback to improve conversions
- Expansion to other statistical conversions (OR to RR, etc.)
- Real-time literature monitoring for LSM studies
- Integration with AI-powered systematic review platforms

### **Scalability**
- Multi-language support for global research community
- Cloud-based processing for large datasets
- Collaborative features for research teams

---

## ⚠️ Limitations

### **Technical Limitations**
- Conversions are approximations with inherent uncertainty
- Requires adequate reporting of study characteristics
- Cannot recover information not reported in original studies
- May not work optimally for highly complex adjusted models

### **Usage Guidelines**
- **Quality Score >80**: High confidence, safe for meta-analysis
- **Quality Score 60-79**: Moderate confidence, use with caution
- **Quality Score <60**: Low confidence, consider excluding or contacting authors

### **Best Practices**
- Always report conversion methodology in systematic reviews
- Contact original authors when possible for raw data
- Use sensitivity analyses to test robustness of converted data

---

## 🛡️ Ethical Statement

### **Data Privacy**
- No user data is stored permanently
- All calculations performed locally
- No transmission of sensitive research data

### **Research Ethics**
- Tool includes disclaimers about conversion limitations
- Recommends contacting original authors when possible
- Promotes transparent reporting of conversion methods

### **Academic Integrity**
- Proper attribution of conversion methodology required
- Citation guidelines provided for academic use
- Open-source approach for transparency and validation

---

## 📞 Support & Contact

### **Technical Support**
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Comprehensive user guide included in app
- **Video Tutorials**: Available on Nibras Research Academy platform

### **Academic Collaboration**
- **Nibras Research Academy**: Training and mentorship in systematic reviews
- **Research Partnerships**: Collaborate on meta-analysis projects
- **Validation Studies**: Contribute to tool improvement research

### **Contact Information**
- **Email**: [Contact through Nibras Research Academy]
- **Institution**: King Edward Medical University, Lahore, Pakistan
- **Conference**: NRIC25 - AI Project Showcase

---

## 🏆 NRIC25 Submission Details

### **Conference**: 1st National Research and Innovation Conference
### **Organizer**: King Edward Medical University, Lahore
### **Category**: AI Project Showcase
### **Submission Deadline**: July 14, 2025
### **Notification**: July 22, 2025

### **Innovation Highlights**
1. **Addresses Real Clinical Research Problem**: LSM conversion is a genuine barrier in evidence synthesis
2. **AI-Enhanced Statistical Processing**: Context-aware algorithms with quality assessment
3. **Immediate Practical Impact**: Usable by KEMU students and researchers today
4. **Scalable Solution**: Can benefit global research community
5. **Evidence-Based Development**: Built by meta-analysis expert who understands user needs

### **Demo Materials**
- **Live Application**: Streamlit web interface
- **Sample Data**: Pre-loaded examples for demonstration
- **Export Capabilities**: Show integration with meta-analysis software
- **Quality Assessment**: Demonstrate reliability scoring system

---

## 📄 File Structure

```
lsm-converter/
├── lsm_converter.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This documentation
├── sample_data/             # Example datasets
│   ├── template.csv         # CSV template for batch processing
│   └── demo_studies.csv     # Sample studies for testing
└── docs/                    # Additional documentation
    ├── user_guide.md        # Detailed usage instructions
    ├── technical_specs.md   # Technical implementation details
    └── validation_study.md  # Validation methodology and results
```

---

## 🎯 Quick Start

1. **Clone/Download** the project files
2. **Install** dependencies: `pip install -r requirements.txt`
3. **Run** the app: `streamlit run lsm_converter.py`
4. **Navigate** to the URL shown in terminal (usually `http://localhost:8501`)
5. **Start converting** LSM data to Mean/SD format!

---

## 📚 References & Citations

### **Statistical Methods**
- Higgins JPT, Thomas J, Chandler J, et al. Cochrane Handbook for Systematic Reviews of Interventions version 6.3
- Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2009.

### **LSM Conversion Methodology**
- Wan X, Wang W, Liu J, Tong T. Estimating the sample mean and standard deviation from the sample size, median, range and/or interquartile range. BMC Med Res Methodol. 2014;14:135.

### **Software Citation**
```
Saddique MN. LSM to Mean/SD Converter: AI-Powered Statistical Tool for Meta-Analysis. 
Version 1.0. King Edward Medical University; 2025. 
Presented at: NRIC25, Lahore, Pakistan.
```

---

*Developed for NRIC25 - King Edward Medical University, Lahore, Pakistan*  
*© 2025 Muhammad Nabeel Saddique | Nibras Research Academy*