name: CTest
Version: 1.0
Release: 1%{?dist}
Summary: The "CTest" program from GNU
License: GPLv3+
Source0: %{name}.tar.gz

%description
The "CTest" program

# rpm安装前执行的脚本
# 作用: cd /root/rpmbuild/BUILD/CTest/
%prep
%setup -n CTest

# rpm安装后执行的脚本
%post

# rpm卸载前执行的脚本
%preun

# rpm卸载后执行的脚本
%postun

# build默认 cd /root/rpmbuild/BUILD/CTest/ 目录下
%build
mkdir build
cd build
cmake ..
make %{?_smp_mflags}

# install默认 cd /root/rpmbuild/BUILD/CTest/ 目录下
# 开始把软件安装到虚拟的根目录中，正规写法应该是在MakeFile里面些install
# 虚拟根目录即 /root/rpmbuild/BUILDROOT/’包名‘
# 可以用宏 $RPM_BUILD_ROOT 或 %{buildroot} 代替
%install
mkdir -p %{buildroot}%{_bindir}
cd build
cp CTest %{buildroot}%{_bindir}

# files能指定最终打包到安装包的文件
# !!files默认 cd /root/rpmbuild/BUILDROOT/'包名'/ 目录下
# %defattr(文件权限,用户名,组名,目录权限),其中'-'表示默认权限
%files
%defattr(-,root,root,-)
%{_bindir}/*
