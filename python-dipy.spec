%global modname dipy

Name:           python-%{modname}
Version:        0.9.2
Release:        1%{?dist}
Summary:        Diffusion magnetic resonance imaging (dMRI) analysis

License:        BSD
URL:            http://dipy.org/
Source0:        https://github.com/nipy/dipy/archive/%{version}/%{modname}-%{version}.tar.gz
# https://github.com/nipy/dipy/pull/731
Patch0:         0001-BF-Another-use-of-a-ufunc-across-types-with-inline-a.patch
Patch1:         0002-BF-For-numpy-1.6-we-might-need-to-cast-this-as-float.patch
BuildRequires:  git-core
# For matplotlib tests
BuildRequires:  /usr/bin/xvfb-run

%description
Here are just a few of the state-of-the-art technologies and algorithms which
are provided in Dipy:

* Reconstruction algorithms e.g. CSD, DSI, GQI, DTI, QBI and SHORE.
* Fiber tracking algorithms e.g. Deterministic, Probabilistic.
* Simple interactive visualization of ODFs and streamlines.
* Apply different operations on streamlines.
* Simplify large datasets of streamlines using QuickBundles clustering.
* Reslice datasets with anisotropic voxels to isotropic.
* Calculate distances/correspondences between streamlines.
* Deal with huge streamline datasets without memory restrictions (.dpy).

With the help of some external tools you can also:

* Read many different file formats e.g. Trackvis or Nifti (with nibabel).
* Examine your datasets interactively (with ipython).

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel python-setuptools python-six
BuildRequires:  numpy
BuildRequires:  Cython
BuildRequires:  python2-nibabel
# Test deps
BuildRequires:  python-nose
BuildRequires:  python-matplotlib python-scikit-learn python-tables vtk-python python-cvxopt
Requires:       python-six
Requires:       numpy scipy
Requires:       python2-nibabel
Recommends:     python-Traits
Recommends:     python-matplotlib
Recommends:     python-scikit-learn
Recommends:     python-tables
Recommends:     vtk-python
Recommends:     python-cvxopt

%description -n python2-%{modname}
Here are just a few of the state-of-the-art technologies and algorithms which
are provided in Dipy:

* Reconstruction algorithms e.g. CSD, DSI, GQI, DTI, QBI and SHORE.
* Fiber tracking algorithms e.g. Deterministic, Probabilistic.
* Simple interactive visualization of ODFs and streamlines.
* Apply different operations on streamlines.
* Simplify large datasets of streamlines using QuickBundles clustering.
* Reslice datasets with anisotropic voxels to isotropic.
* Calculate distances/correspondences between streamlines.
* Deal with huge streamline datasets without memory restrictions (.dpy).

With the help of some external tools you can also:

* Read many different file formats e.g. Trackvis or Nifti (with nibabel).
* Examine your datasets interactively (with ipython).

Python 2 version.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel python3-setuptools python3-six
BuildRequires:  python3-numpy
BuildRequires:  python3-Cython
BuildRequires:  python3-nibabel
# Test deps
BuildRequires:  python3-nose
BuildRequires:  python3-matplotlib python3-scikit-learn python3-tables python3-cvxopt
Requires:       python3-six
Requires:       python3-numpy python3-scipy
Requires:       python3-nibabel
Recommends:     python3-Traits
Recommends:     python3-matplotlib
Recommends:     python3-scikit-learn
Recommends:     python3-tables
#TODO: Recommends:     vtk-python3
Recommends:     python3-cvxopt

%description -n python3-%{modname}
Here are just a few of the state-of-the-art technologies and algorithms which
are provided in Dipy:

* Reconstruction algorithms e.g. CSD, DSI, GQI, DTI, QBI and SHORE.
* Fiber tracking algorithms e.g. Deterministic, Probabilistic.
* Simple interactive visualization of ODFs and streamlines.
* Apply different operations on streamlines.
* Simplify large datasets of streamlines using QuickBundles clustering.
* Reslice datasets with anisotropic voxels to isotropic.
* Calculate distances/correspondences between streamlines.
* Deal with huge streamline datasets without memory restrictions (.dpy).

With the help of some external tools you can also:

* Read many different file formats e.g. Trackvis or Nifti (with nibabel).
* Examine your datasets interactively (with ipython).

Python 3 version.

%prep
%autosetup -n %{modname}-%{version} -S git
find -type f -regex '.*\.py[x]*' -exec sed -i \
  -e "s/from \.*utils.six/from six/" \
  -e "s/from dipy.utils.six/from six/" \
  {} ';'
rm -f dipy/utils/six.py

rm -rf %{py3dir}
mkdir -p %{py3dir}
cp -a . %{py3dir}
for mod in dipy_fit_tensor dipy_peak_extraction dipy_quickbundles dipy_sh_estimate
do
  sed -i -e "/cmd =/s/$mod/$mod-2/" dipy/tests/test_scripts.py
  sed -i -e "/cmd =/s/$mod/$mod-3/" %{py3dir}/dipy/tests/test_scripts.py
done

%build
%py2_build
pushd %{py3dir}
  %py3_build
popd

%install
pushd %{py3dir}
  %py3_install
popd
%py2_install

# Rename binaries
pushd %{buildroot}%{_bindir}
  for mod in dipy_fit_tensor dipy_peak_extraction dipy_quickbundles dipy_sh_estimate
  do
    mv $mod python2-$mod

    sed -i '1s|^.*$|#!/usr/bin/env %{__python2}|' python2-$mod
    for i in $mod $mod-2 $mod-%{python2_version}
    do
      ln -s python2-$mod $i
    done

    cp python2-$mod python3-$mod
    sed -i '1s|^.*$|#!/usr/bin/env %{__python3}|' python3-$mod

    for i in $mod-3 $mod-%{python3_version}
    do
      ln -s python3-$mod $i
    done
  done
popd

%check
# Don't fail here, it wants to run installed commands
PYTHONPATH=%{buildroot}%{python2_sitearch} \
PATH="%{buildroot}%{_bindir}:$PATH" \
  xvfb-run nosetests-%{python2_version} -v build/lib.*-%{python2_version} || :
pushd %{py3dir}
  PYTHONPATH=%{buildroot}%{python3_sitearch} \
  PATH="%{buildroot}%{_bindir}:$PATH" \
    xvfb-run nosetests-%{python3_version} -v build/lib.*-%{python3_version} || :
popd

%files -n python2-%{modname}
%license LICENSE
%doc README.rst AUTHOR doc/examples
%{_bindir}/python2-dipy_fit_tensor
%{_bindir}/dipy_fit_tensor
%{_bindir}/dipy_fit_tensor-2
%{_bindir}/dipy_fit_tensor-%{python2_version}
%{_bindir}/python2-dipy_peak_extraction
%{_bindir}/dipy_peak_extraction
%{_bindir}/dipy_peak_extraction-2
%{_bindir}/dipy_peak_extraction-%{python2_version}
%{_bindir}/python2-dipy_quickbundles
%{_bindir}/dipy_quickbundles
%{_bindir}/dipy_quickbundles-2
%{_bindir}/dipy_quickbundles-%{python2_version}
%{_bindir}/python2-dipy_sh_estimate
%{_bindir}/dipy_sh_estimate
%{_bindir}/dipy_sh_estimate-2
%{_bindir}/dipy_sh_estimate-%{python2_version}
%{python2_sitearch}/%{modname}*

%files -n python3-%{modname}
%license LICENSE
%doc README.rst AUTHOR doc/examples
%{_bindir}/python3-dipy_fit_tensor
%{_bindir}/dipy_fit_tensor-3
%{_bindir}/dipy_fit_tensor-%{python3_version}
%{_bindir}/python3-dipy_peak_extraction
%{_bindir}/dipy_peak_extraction-3
%{_bindir}/dipy_peak_extraction-%{python3_version}
%{_bindir}/python3-dipy_quickbundles
%{_bindir}/dipy_quickbundles-3
%{_bindir}/dipy_quickbundles-%{python3_version}
%{_bindir}/python3-dipy_sh_estimate
%{_bindir}/dipy_sh_estimate-3
%{_bindir}/dipy_sh_estimate-%{python3_version}
%{python3_sitearch}/%{modname}*

%changelog
* Sat Oct 31 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.2-1
- Initial package
