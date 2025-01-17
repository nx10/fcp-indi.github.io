Amplitude of Low Frequency Fluctuations (ALFF) and fractional ALFF (f/ALFF)
---------------------------------------------------------------------------

Introduction & Background
^^^^^^^^^^^^^^^^^^^^^^^^^
Slow fluctuations in activity are a fundamental feature of the resting brain, and their presence is key to determining correlated activity between brain regions and defining resting state networks. The relative magnitude of these fluctuations can differ between brain regions and between subjects, and thus may act as a marker of individual differences or dysfunction. **Amplitude of Low Frequency Fluctuations** `(ALFF; Zang et al., 2007) <http://www.ncbi.nlm.nih.gov/pubmed/16919409>`_ and **fractional Amplitude of Low Frequency Fluctuations** `(f/ALFF; Zou et al., 2008) <http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3902859/>`_ are related measures that quantify the amplitude of these low frequency oscillations (LFOs).

ALFF is defined as the total power within the frequency range between 0.01 and 0.1 Hz, and thus indexes the strength or intensity of LFO. f/ALFF is defined as the power within the low-frequency range (0.01-0.1 Hz) divided by the total power in the entire detectable frequency range, and represents the relative contribution of specific LFO to the whole frequency range (Zuo et al., 2010).

Computation and Analysis Considerations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All computations are performed in a subject's native space. After transforming voxel time series frequency information into the power domain, calculation of these measures is relatively simple. ALFF is calculated as the sum of amplitudes within a specific low frequency range. f/ALFF is calculated as a fraction of the sum of amplitudes across the entire frequency range detectable in a given signal. For both measures, amplitudes in subject-level maps are transformed into Z-scores to create standardized subject-level maps. Anatomical images and Z-score maps are then transformed into MNI152 standard space. For more detail on how CPAC computes these steps, please see the `ALFF and f/ALFF Page of the developer documentation <http://fcp-indi.github.io/docs/developer/workflows/alff.html>`_.

Though both ALFF and f/ALFF are sensitive mostly to signal from gray matter, ALFF is more prone to noise from physiological sources, particularly near the ventricles and large blood vessels (Zuo et al., 2008;2010). The figure below (from Zuo et al., 2010) shows areas in which ALFF shows higher amplitude than f/ALFF, as well as the relative sensitivity of these measures to gray matter.

.. figure:: /_images/alff_zuo_difference.png

Both ALFF and f/ALFF show moderate to high test-retest reliability in gray matter regions, but reliability for ALFF tends to be higher than for fALFF (Zuo et al., 2010). As it is more reliable, ALFF may be more sensitive to differences between groups and individuals. The figure below (also from Zuo et al., 2010) shows differences in test-retest reliability as measured by Intraclass Correlation (ICC; Shrout and Fleiss, 1979).

.. figure:: /_images/alff_zuo_trt.png

Finally, as these measures require a constant timecourse on which to do frequency and power analyses, they cannot be run on scrubbed data (Power et al., 2012) in which volumes with excessive movement have been removed.

Applications and Recommendations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ALFF and f/ALFF have been used to uncover differences in amplitude power both between subjects and between conditions. Zang et al. (2007) found that children with ADHD show reduced ALFF amplitude in some brain areas and increased amplitude in others compared to controls, while Yan and colleagues (2009) saw increased amplitude in the Default Mode Network during Eyes Open vs. Eyes Closed resting periods. Changes in f/ALFF have also been observed with aging (Hu et al., 2013).

The increased specificity to the gray matter signal for f/ALFF compared to ALFF may suggest favoring the former, but doing so would come at the cost of reduced test-retest reliability. As such, in order to maximize the reliability across subjects while providing sufficient specificity to examine individual differences, reporting both measures is recommended (Zuo et al., 2010).

Configuring CPAC to Run ALFF and f/ALFF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. figure:: /_images/alff_gui.png

#. **ALFF / f/ALFF - [Off, On]:** Calculate Amplitude of Low Frequency Fluctuations (ALFF) and and fractional ALFF (f/ALFF) for all voxels.

#. **f/ALFF High-Pass Cutoff - [decimal]:** Frequency cutoff (in Hz) for the high-pass filter used when calculating f/ALFF.

#. **f/ALFF Low-Pass Cutoff - [decimal]:** Frequency cutoff (in Hz) for the low-pass filter used when calculating f/ALFF

.. include:: /user/pipelines/without_gui.rst

.. literalinclude:: /references/default_pipeline.yml
   :language: YAML
   :start-at: amplitude_low_frequency_fluctuation:
   :end-before: regional_homogeneity:

References
^^^^^^^^^^
Power, J. D., Barnes, K. A., Snyder, A. Z., Schlaggar, B. L., & Petersen, S. E. (2012). `Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion <http://www.ncbi.nlm.nih.gov/pubmed/22019881>`_. Neuroimage, 59(3), 2142–2154. 

Sien Hu, Herta H.-A. Chao, Sheng Zhang, Jaime S. Ide, Chiang-Shan R. Li (2013), `Changes in cerebral morphometry and amplitude of low-frequency fluctuations of BOLD signals during healthy aging: correlation with inhibitory control <http://link.springer.com/content/pdf/10.1007%2Fs00429-013-0548-0.pdf>`_. Brain Structure and Function

Shrout, P.E., Fleiss, J.L., 1979. `Intraclass correlations: uses in assessing rater reliability <http://www.ncbi.nlm.nih.gov/pubmed/18839484>`_.
Psychol. Bull. 86, 420–428.

Zang, Y.-F., He, Y., Zhu, C.-Z., Cao, Q.-J., Sui, M.-Q., Liang, M., Tian, L.-X., et al. (2007). `Altered baseline brain activity in children with ADHD revealed by resting-state functional MRI <http://nlpr-web.ia.ac.cn/2007papers/gjkw/gk38.pdf>`_. Brain & development, 29(2), 83–91.

Zou, Q.-H., Zhu, C.-Z., Yang, Y., Zuo, X.-N., Long, X.-Y., Cao, Q.-J., Wang, Y.-F., et al. (2008). `An improved approach to detection of amplitude of low-frequency fluctuation (ALFF) for resting-state fMRI: Fractional ALFF <http://www.nlpr.labs.gov.cn/2008papers/gjkw/gk26.pdf>`_. Journal of neuroscience methods, 172(1), 137–141.

Zuo, X.-N., Di Martino, A., Kelly, C., Shehzad, Z. E., Gee, D. G., Klein, D. F., Castellanos, F. X., et al. (2010). `The oscillating brain: complex and reliable <http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2856476/>`_. Neuroimage, 49(2), 1432–1445. 
