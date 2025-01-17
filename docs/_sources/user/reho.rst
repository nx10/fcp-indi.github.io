﻿Regional Homogeneity
--------------------

Introduction & Background
^^^^^^^^^^^^^^^^^^^^^^^^^
Regional Homogeneity (ReHo) is a voxel-based measure of brain activity which evaluates the similarity or synchronization between the time series of a given voxel and its nearest neighbors (Zang et al., 2004). This measure is based on the hypothesis that intrinsic brain activity is manifested by clusters of voxels rather than single voxels. Kendall's coefficient of concordance (KCC) (Kendall and Gibbons, 1990) is used as an index to evaluate the similarity of the time series within a cluster of a given voxel and its nearest neighbors. ReHo requires no *a priori* definition of ROIs and can provide information about the local/regional activity of regions throughout the brain.

.. figure:: /_images/reho_yan_dmn.png

The figure above (taken from Yan and Zang, 2010) shows the default mode network as detected by ReHo analysis (colors indicate *t* values).

Computation and Analysis Considerations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KCC is computed for every voxel in a subject, and is based on the time series of each voxel, the number of time points within a time series, and the number of voxels within a cluster (Zang et al, 2004). Depending on whether neighboring voxels are taken to include those on the side, edge, or corner of a given voxel, cluster size can be 7, 19, or 27 voxels, respectively. Values of KCC range from 0 to 1, with higher values indicating greater similarity between the activation pattern of a given voxel and that of its neighbors. Voxel-based maps are generated based on KCC values and then standardized using Z-scores in order to perform group analysis. For more detail on how CPAC handles these computations, please see the `ReHo section of the developer documentation <http://fcp-indi.github.io/docs/developer/workflows/reho.html>`_.

.. figure:: /_images/reho_voxel_schematic.png

The results of ReHo analysis have been shown to vary significantly depending on both the number of neighbors in a cluster and the amount of spatial smoothing applied to the data. For example, Zang and colleagues (2004) found more neighbors and greater smoothing to yield greater differences between conditions in a motor task. 

Applications and Recommendations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ReHo as an index of ongoing activity has been widely used in the resting-state literature. ReHo in the Default Mode Network (DMN) has been observed to increase during rest (Long et al., 2008) and decrease during task engagement (Zang et al., 2004), findings that fit well with the existing literature. In healthy subjects, ReHo measures are associated with individual differences in behavioral inhibition (Tian et al., 2012) and normal aging (Wu et al., 2007). In patient populations, altered ReHo has been observed in multiple conditions, including Alzheimer's Disease (Liu et al., 2008), ADHD (Cao et al., 2006), and schizophrenia (Liu et al., 2006).

ReHo analysis can also be applied to task evoked fMRI data and is appropriate for application in block-based and slow event-related designs, but may not provide reliable results in rapid event-related studies. In such paradigms, the hemodynamic signal for a given timepoint is the result of multiple trials, and ReHo is unable to account for this overlapping of signals.

Configuring CPAC to Run ReHo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. figure:: /_images/reho_gui.png

#. **Regional Homogeneity (ReHo) - [Off, On]:** Calculate Regional Homogeneity (ReHo) for all voxels.

#. **Voxel Cluster Size - [7,19,27]:** Number of neighboring voxels used when calculating ReHo. 7 (Faces), 19 (Faces + Edges), or 27 (Faces + Edges + Corners).

.. include:: /user/pipelines/without_gui.rst

.. literalinclude:: /references/default_pipeline.yml
   :language: YAML
   :start-at: regional_homogeneity:
   :end-before: voxel_mirrored_homotopic_connectivity:

References
^^^^^^^^^^
Cao, Q., Zang, Y., Sun, L., Sui, M., Long, X., Zou, Q., Wang, Y., 2006. `Abnormal neural activity in children with attention deficit hyperactivity disorder: a resting-state functional magnetic resonance imaging study <http://www.ncbi.nlm.nih.gov/pubmed/16791098>`_. Neuroreport 17, 1033-1036.

He, Y., Wang, L., Zang, Y., Tian, L., Zhang, X., Li, K., Jiang, T., 2007. `Regional coherence changes in the early stages of Alzheimer's disease: a combined structural and resting-state functional MRI study <http://www.ncbi.nlm.nih.gov/pubmed/17254803>`_. Neuroimage 35, 488-500. 

Kendall, M.G., Gibbons, J.D., 1990. Rank Correlation Methods, 5th ed. Oxford University Press.

Liu, H., Liu, Z., Liang, M., Hao, Y., Tan, L., Kuang, F., Yi, Y., Xu, L., Jiang, T., 2006. `Decreased regional homogeneity in schizophrenia: a resting state functional magnetic resonance imaging study <http://www.nlpr.ia.ac.cn/2006papers/gjkw/gk21.pdf>`_. Neuroreport 17, 19-22. 

Wu, T., Zang, Y., Wang, L., Long, X., Hallett, M., Chen, Y., Li, K., Chan, P., 2007. `Normal aging decreases regional homogeneity of the motor areas in the resting state <http://www.sciencedirect.com/science/article/pii/S0304394007007252>`_. Neurosci Lett 422, 164-168. 

Xiang-Yu Long, Xi-Nian Zuo, Vesa Kiviniemi, Yihong Yang, Qi-Hong Zou, Chao-Zhe Zhu, Tian-Zi Jiang, Hong Yang, Qi-Yong Gong, LiangWang, Kun-Cheng Li, Sheng Xie, Yu-Feng Zang. `Default mode network as revealed with multiple methods for resting-state functional MRI analysis <http://psychbrain.bnu.edu.cn/home/chaozhezhu/paper/Long_NeuroImage2008.pdf>`_, J Neurosci Methods (2008), 171(2):349-55

Yan, C.-G., & Zang, Y.-F. (2010). `DPARSF: A MATLAB Toolbox for “Pipeline” Data Analysis of Resting-State fMRI <http://www.frontiersin.org/systems_neuroscience/10.3389/fnsys.2010.00013/>`_. Frontiers in systems neuroscience, 4, 13. doi:10.3389/fnsys.2010.00013

Zang, Y., Jiang, T., Lu, Y., He, Y., Tian, L., 2004. `Regional homogeneity approach to fMRI data analysis <http://nlpr-web.ia.ac.cn/english/mic/Zang_NI04.pdf>`_. Neuroimage 22, 394-400. 
